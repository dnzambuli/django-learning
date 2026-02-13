"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# import redirect view to redirect root url to api urls
# from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # for authentication and user management
    path('auth/', include('djoser.urls')),  # djoser urls for user registration and authentication
    path('auth/', include('djoser.urls.authtoken')),  # djos

    # for my app
    path('api/', include('taskmanager.urls')),  # include urls from taskmanager app
    # path('', RedirectView.as_view(url='/api/', permanent=False)),  # redirect root url to api urls
]
