from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<int:pk>/', views.menu_item_detail, name='menu_item_detail'),
]
