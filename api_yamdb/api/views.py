from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from titles.models import Category, Genre, Title
from rest_framework import viewsets


#from .permissions import 
from .permissions import (AdminModeratorAuthorPermission,)
from reviews.models import Review
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWhiteSerializer,
                          CommentSerializer, ReviewSerializer,
                          )


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
