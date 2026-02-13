from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet # , CustomUserViewS

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task') # register TaskViewSet
# router.register(r'users', CustomUserViewSet, basename='user') # register CustomUserViewSet

urlpatterns = [
    path('task/', include(router.urls)), # include the router urls
]