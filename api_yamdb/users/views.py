from multiprocessing import context

from api.permissions import IsAdminOrUserReadOnly
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import (
    ConfirmationCodeSerializer,
    EmailSerializer,
    MeSerializer,
    UserSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    mail_subject = f"Код подтверждения для {username}"
    sender = "Vasya Pupkin"
    adress = [email]

    check_email = User.objects.filter(email=email)
    check_username = User.objects.filter(username=username)
    if (check_username and not check_email) or (
        not check_username and check_email
    ):
        context = {"error": "username or email has already been created"}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.get_or_create(username=username, email=email)
        print(user, "THIS IS user", type(user))
        confirmation_code = default_token_generator.make_token(user[0])
        print(confirmation_code)
        message = f"Ваш {mail_subject}: {confirmation_code}"
        send_mail(mail_subject, message, sender, adress)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def auth_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, code):
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
    return Response(
        {"token": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminOrUserReadOnly,
    ]
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
    ]

    @action(
        methods=["patch", "get"],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path="me",
        url_name="me",
    )
    def me(self, request):
        user = self.request.user
        serializer = MeSerializer(user)
        if self.request.method == "PATCH":
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
