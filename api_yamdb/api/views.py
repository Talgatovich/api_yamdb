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

from .filters import TitleFilter
from .permissions import AdminModeratorAuthorPermission, AdminOrReadOnly
from .serializers import (
    AuthenticationSerializer,
    CategorySerializer,
    CommentSerializer,
    ConfirmationCodeSerializer,
    GenreSerializer,
    MeSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
)

from api.permissions import IsAdminOrUserReadOnly  # isort:skip
from reviews.models import Review  # isort:skip
from titles.models import Category, Genre, Title  # isort:skip
from users.models import User  # isort:skip


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


class CDLViewSet(
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


class CategoryViewSet(CDLViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CDLViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
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
    serializer = AuthenticationSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    mail_subject = f"?????? ?????????????????????????? ?????? {username}"
    sender = settings.DEFAULT_EMAIL_SENDER
    adress = [email]
    try:
        user = User.objects.get_or_create(username=username, email=email)
    except Exception:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user[0])
    message = f"?????? {mail_subject}: {confirmation_code}"
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
        serializer = MeSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if self.request.method != "PATCH":
            serializer = MeSerializer(user)
        return Response(serializer.data)
