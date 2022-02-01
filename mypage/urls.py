from django.urls import path, include
from mypage import views

urlpatterns = [
    path('', views.landing),

]