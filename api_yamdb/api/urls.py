from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register("categories", CategoryViewSet)
#router.register("genres", GenresViewSet)
#router.register("titles", TitlesViewSet)
#router.register(
#    r"^titles\/(?P<id>\d+)\/reviews", ReviewViewSet, basename="reviews"
#)


urlpatterns = [
    path('v1/', include(router.urls)),
    path("v1/api-token-auth/", views.obtain_auth_token),
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),


]
