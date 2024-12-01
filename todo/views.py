from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'todo/todo.html')

def register(request):
    return render(request, 'todo/register.html')

def login(request):
    return render(request, 'todo/login.html')