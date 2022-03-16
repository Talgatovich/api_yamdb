from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from titles.models import Category, Genre, Title

#from .permissions import 
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWhiteSerializer)


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
