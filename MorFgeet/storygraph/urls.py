from django.urls import path
from storygraph.views import get_random_node, main_view, node_display

urlpatterns = [
    path("", main_view, name="main"),
    path("node/random/<current_node>", get_random_node, name="random_node"),
    path("node/<id>", node_display, name="node_display"),
]
