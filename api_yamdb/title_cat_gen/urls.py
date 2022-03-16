from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
