from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.signup),
    path('logout/', views.logout, name="logout"),
    path('', views.login, name="login"), # {% url
]