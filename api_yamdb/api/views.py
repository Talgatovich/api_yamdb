from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import User

from api.permissions import IsAdminOrUserReadOnly

from .filters import TitleFilter
from .permissions import AdminModeratorAuthorPermission, AdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationCodeSerializer, EmailSerializer,
                          GenreSerializer, MeSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg("reviews__score"))
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AdminOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    serializer_class = TitleWriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return TitleWriteSerializer
        return TitleReadSerializer


class ForCategoryAndGenre(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AdminOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]
    lookup_field = "slug"


class CategoryViewSet(ForCategoryAndGenre):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ForCategoryAndGenre):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"),
                 title=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"),
                 title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    mail_subject = f"Код подтверждения для {username}"
    sender = settings.DEFAULT_EMAIL_SENDER
    adress = [email]

    check_email = User.objects.filter(email=email)
    check_username = User.objects.filter(username=username)
    if (check_username and not check_email) or (
        not check_username and check_email
    ):
        text = {"error": "username or email has already been created"}
        return Response(text, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.get_or_create(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user[0])
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
