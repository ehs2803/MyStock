from django.urls import path, include
from chat import views

urlpatterns = [
    path('', views.landing),
    
]