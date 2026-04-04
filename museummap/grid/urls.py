from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("save-comment/", views.save_comment, name="save_comment"),
    path("get-comments/", views.get_comments, name="get_comments"),
    path("delete-comments/", views.delete_comments, name="delete_comments")
]