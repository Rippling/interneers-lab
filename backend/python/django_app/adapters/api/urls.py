from django.urls import path
from .views import hello_world

urlpatterns = [
    path("hello-world/", hello_world, name="hello-world")
]
