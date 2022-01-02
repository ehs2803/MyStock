from django.urls import path, include
from board import views

urlpatterns = [
    path('', views.landing),
    path('SE005930/', views.SE005930),
]