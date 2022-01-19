from django.urls import path, include
from board import views

urlpatterns = [
    path('', views.landing),
    path('<code>/', views.BOARD),
    path('<code>/writing/', views.BOARD_writing),
    path('<code>/post/<int:pk>', views.BOARD_post, name='board_post'),
    path('<code>/edit/<int:pk>', views.BOARD_edit),
    path('<code>/delete/<int:pk>', views.BOARD_delete),
    path('<code>/comment/<int:pk>', views.BOARD_comment),
    path('<code>/comment/delete/<int:pk>/<ci>', views.BOARD_comment_delete),
]