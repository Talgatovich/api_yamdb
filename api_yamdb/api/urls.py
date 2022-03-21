from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import AuthToken, UserViewSet, get_confirmation_code

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategoryViewSet, basename="categories")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("users", UserViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", get_confirmation_code),
    path("v1/auth/token/", AuthToken),
]
