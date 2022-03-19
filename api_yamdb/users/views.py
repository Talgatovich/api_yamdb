from api.my_functions import random_code
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import ConfirmationCodeSerializer, EmailSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        confirmation_code = random_code()
        User.objects.get_or_create(username=username, email=email)
        User.objects.filter(email=email).update(
            confirmation_code=confirmation_code
        )
        mail_subject = "Код подтверждения"
        message = f"Ваш {mail_subject}: {confirmation_code}"
        sender = "Vasya Pupkin"
        adress = [email]

        send_mail(mail_subject, message, sender, adress)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def AuthToken(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(
            User, username=username, confirmation_code=code
        )
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
