from django.urls import path, include
from rest_framework.routers import DefaultRouter
from image_app.views import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
