from django.shortcuts import render
from .models import User

# Create your views here.

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {"users": users})

# from django.http import HttpResponse
# from pathlib import Path
#
# def index(request):
#     path = Path(__file__).resolve()
#     return HttpResponse(f"VIEW FILE: {path}")
