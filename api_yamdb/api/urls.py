from django.urls import include, path
<<<<<<< HEAD
from rest_framework.routers import SimpleRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

app_name = 'api'

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
=======
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
#router.register(
#    r"^titles\/(?P<id>\d+)\/reviews", ReviewViewSet, basename="reviews"
#)

urlpatterns = [
    
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("v1/api-token-auth/", views.obtain_auth_token),
    path("v1/", include(router.urls))
    #path("v1/auth/signup/", )
]
>>>>>>> 11b2a857f06141ac901b9a929bbaa8ffb0107c7b
