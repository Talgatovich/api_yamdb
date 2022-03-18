from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomAuthToken, get_confirmation_code

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router = DefaultRouter()
router.register("titles", TitleViewSet)
router.register("genres", GenreViewSet)
router.register("categories", CategoryViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", get_confirmation_code),
    path("v1/auth/token/", CustomAuthToken.as_view()),
]
