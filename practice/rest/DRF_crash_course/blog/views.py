from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer

# DRF automatically handles the GET/PUT/POST apis in this (recall all the code we had to write to manually make apis)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
