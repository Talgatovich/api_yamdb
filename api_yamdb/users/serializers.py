from api.my_functions import random_code
from django.core.mail import send_mail
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        """
        Проверка существования юзера с переданными в запросе e-mail и username.
        Если юзер есть в БД, отправляем новый код на его e-mail и обновляем
        код в самом объекте юзера

        """
        username = data.get("username")
        email = data.get("email")
        confirmation_code = random_code()
        user = User.objects.filter(username=username, email=email)
        sender = "Vasya"
        message = f"Ваш новый код : {confirmation_code}"
        mail_subject = "confirmation_code"
        if user:
            user.update(confirmation_code=confirmation_code)
            send_mail(mail_subject, message, sender, [email])
            raise serializers.ValidationError(
                (
                    "Этот пользователь уже существует.Обновленный код отправлен"
                    "на e-mail"
                )
            )
        return data

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Используйте другой username")
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class MeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        )
