from api.my_functions import random_code
from api.permissions import AdminOrReadOnly, IsAdminOrUserReadOnly
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
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
    confirmation_code = random_code()

    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        check_email = User.objects.filter(email=email)
        check_user = User.objects.filter(username=username)
        if check_user or check_email:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            User.objects.create(username=username, email=email)
            User.objects.filter(email=email).update(
                confirmation_code=confirmation_code
            )
            mail_subject = f"Код подтверждения для {username}"
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
        check_user = User.objects.filter(username=username)
        if not check_user:
            return Response(
                serializer.errors, status=status.HTTP_404_NOT_FOUND
            )
        user = User.objects.get(username=username)
        if user.confirmation_code == code:
            token = AccessToken.for_user(user)
            return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminOrUserReadOnly,
    ]  # (IsAdminUser,)IsAuthenticated
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
