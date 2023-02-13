from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import BotViewSet


router = DefaultRouter()
router.register("", BotViewSet, basename="bot")


urlpatterns = [
    path("", include(router.urls))
]