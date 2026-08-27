"""
URL configuration for restaurant_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from restaurant_site.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('pages.urls')),
    path('menu/', include('menu.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
