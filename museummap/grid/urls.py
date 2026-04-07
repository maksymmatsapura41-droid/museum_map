from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("save-comment/", views.save_comment, name="save_comment"),
    path("get-comments/", views.get_comments, name="get_comments"),
    path("delete-comment/", views.delete_comment, name="delete_comment"),
    path("save-route/", views.save_route, name="save_route"),
    path("get-routes/", views.get_routes, name="get_routes"),
    path("get-route/<int:route_id>/", views.get_route_detail, name="get_route_detail"),
    path("shared-coordinates/", views.get_shared_coordinates, name="get_shared_coordinates"),
    path("shared-coordinate-detail/", views.get_shared_coordinate_detail, name="get_shared_coordinate_detail"),
    path("save-drawing/", views.save_drawing, name="save_drawing"),
    path("get-drawings/", views.get_drawings, name="get_drawings"),
]