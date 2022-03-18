from api_yamdb import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import User

from .my_functions import random_code
from .permissions import AdminModeratorAuthorPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailSerializer, GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWhiteSerializer,
                          UserSerializer)


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)

    serializer.is_valid()
    username = request.data.get('username')
    print("ЭТО ЮЗЕРНЕЙМ",username)
    print("ЭТО ДАТА",request.data)
    print("ЭТО ВАЛИДАТЕД ДАТА",serializer.validated_data)
    email = serializer.validated_data.get('email')
    user = User.objects.get_or_create(username=username, email=email)    
    confirmation_code = random_code()

    mail_subject = 'Код подтверждения'
    message = f'Ваш {mail_subject}: {confirmation_code}'
    sender = 'Vasya Pupkin'
    adress = [email]

    send_mail(
        mail_subject,
        message,
        sender,
        adress
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    #permission_classes = админ на запись, остальные чтение
    pagination_class = LimitOffsetPagination
    
    def get_serializer_class(self):
        # Если запрошенное действие (action) — получение списка объектов ('list')
        # 'retrieve' - получение одного объекта
        if self.action == 'list' or self.action == 'retrieve':
            # ...то применяем TitleReadSerializer
            return TitleReadSerializer
        # А если запрошенное действие — не 'list', 'retrieve'
        # применяем TitleWhiteSerializer
        return TitleWhiteSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = админ на запись, остальные чтение


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = админ на запись, остальные чтение

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
