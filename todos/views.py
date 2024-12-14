from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Home Page View
def home(request):
    return render(request, 'home.html')

# Login Page View
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todo')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login_page.html')

    return render(request, 'login_page.html')

# Registration Page View
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validations
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login-page')

    return render(request, 'register.html')

# Logout View
def logout_page(request):
    logout(request)
    return redirect('home')

# To-Do List View
@login_required(login_url='login-page')
def todo(request):
    if request.method == 'POST' and 'add_task' in request.POST:
        # Add a new task
        add_task = request.POST['add_task']
        Task.objects.create(title=add_task, user=request.user)
        return redirect('todo')

    # Fetch tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo.html', {'tasks': tasks})

# Delete Task View
@login_required(login_url='login-page')
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return redirect('todo')



@login_required(login_url='login-page')
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.save()
        return redirect('todo')
    return render(request, 'edit_task.html', {'task': task})
    