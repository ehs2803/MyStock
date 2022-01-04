from django.urls import path, include
from board import views

urlpatterns = [
    path('', views.landing),
    path('SE005930/', views.SE005930),
    path('SE005930/writing/', views.board_SE005930_writing),
    path('SE005930/post/<int:pk>', views.board_SE005930_post, name='board_post'),
    path('SE005930/edit/<int:pk>', views.board_SE005930_edit),
    path('SE005930/delete/<int:pk>', views.board_SE005930_delete),
    path('SE005930/comment/<int:pk>', views.board_SE005930_comment),
    path('SE005930/delete/comment/<int:pk>/<date>', views.comment_SE005930_delete),
]