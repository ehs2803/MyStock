from django.urls import path
from articles import views

urlpatterns = [
    path('', views.landing),
    path('SE005930/', views.SE005930),
    path('SE000660/', views.SE000660),
    path('SE035420/', views.SE035420),
    path('SE005380/', views.SE005380),
    path('SE091990/', views.SE091990),
    path('SE247540/', views.SE247540),
    path('SE263750/', views.SE263750),
    path('SE293490/', views.SE293490),
]