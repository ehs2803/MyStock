from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.signup),
    path('logout/', views.logout),
    path('', views.login, name="login"),
]