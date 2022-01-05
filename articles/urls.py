from django.urls import path
from articles import views

urlpatterns = [
    path('', views.landing),
    path('SE005930/', views.SE005930),
]