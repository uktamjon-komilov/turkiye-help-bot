from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("bot/", include("bot.urls")),
    path("admin/", admin.site.urls),
]
