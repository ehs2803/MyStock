from django.urls import path, include
from chat import views

urlpatterns = [
    path('', views.landing),
    path('<str:room_name>/', views.room, name='room'),
]