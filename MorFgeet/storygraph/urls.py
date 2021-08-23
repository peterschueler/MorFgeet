from django.urls import path
from storygraph.views import main_view, node_display

urlpatterns = [
    path("", main_view, name="main"),
    path("node/<id>", node_display, name="node_display"),
]
