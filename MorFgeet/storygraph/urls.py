from django.urls import path
from storygraph.views import main_view

urlpatterns = [path("", main_view, name="main")]
