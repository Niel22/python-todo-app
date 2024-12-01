from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Todo
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
# Home
@login_required
def home(request):
    todos = Todo.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo/todo.html', {'todos' : todos})

# Register
def register(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        if len(password) < 8:
            messages.error(request, 'Password is too short, minimum of 8 charachters')
            return redirect('register')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todo/register.html', {})

# Login
def login(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        validated_user = authenticate(username=username, password=password)
        if validated_user is not None:
            auth_login(request, validated_user)
            return redirect('home')
        
        messages.error(request, 'Invalid username or password')
        return redirect('login')
    
    return render(request, 'todo/login.html', {})

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'We hope to see you soon')
    return redirect('login')

# Create task
@login_required
def add_todo(request):
    if request.method == "POST":
        name = request.POST.get('name')
        new_todo = Todo(user=request.user, name=name)
        new_todo.save()

        messages.success(request, "Task added")
        return redirect('home')

# Delete Task
@login_required
def delete_todo(request, id):
    try:
        task = Todo.objects.get(user=request.user, id=id)
        task.delete()
        messages.success(request, 'Task Deleted')
        return redirect('home')
    except Todo.DoesNotExist:
        messages.error(request, 'Task Does not exist')
        return redirect('home')

# Update Task
@login_required
def update_todo(request, id):
    try:
        task = Todo.objects.get(user=request.user, id=id)
        task.status = True
        task.save()
        messages.success(request, 'Task Updated to completed')
        return redirect('home')
    except Todo.DoesNotExist:
        messages.error(request, 'Task Does not exist')
        return redirect('home')