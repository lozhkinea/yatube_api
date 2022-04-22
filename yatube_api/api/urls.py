from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api import views

app_name = "api"

v1_router = routers.DefaultRouter()
v1_router.register(r"v1/posts", views.PostViewSet)
v1_router.register(
    r"v1/posts/(?P<post_id>\d+)/comments",
    views.CommentViewSet,
    basename="comment",
)
v1_router.register(r"v1/groups", views.GroupViewSet)


urlpatterns = [
    path(
        "v1/jwt/create/",
        TokenObtainPairView.as_view(),
        name="token_create",
    ),
    path("v1/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(v1_router.urls)),
    path(
        "v1/follow/",
        views.FollowViewSet.as_view({"get": "list", "post": "create"}),
    ),
]
