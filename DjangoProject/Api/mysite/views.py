from django.shortcuts import render

# django rest frameworks to provide default views
from rest_framework.views import generics

# import the model made
from .models import BlogPost

# import the model serializer
from serializers import BlogPostSerializer


# Create your views here.
class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

