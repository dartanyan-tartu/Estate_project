from django.shortcuts import render, get_object_or_404
# properties/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Employee
from .forms import RegisterForm

def index(request):
    properties = Property.objects.filter(is_published=True)
    return render(request, 'properties/index.html', {'properties': properties})

def property_detail(request, prop_id):
    property = get_object_or_404(Property, id=prop_id, is_published=True)
    return render(request, 'properties/property_detail.html', {'property': property})

def team(request):
    employees = Employee.objects.filter(is_active=True).order_by('created_at')
    return render(request, 'properties/team.html', {'employees': employees})

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Исправьте ошибки ниже.')
    else:
        form = RegisterForm()
    return render(request, 'properties/register.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'properties/login.html')

@login_required
def profile_page(request):
    return render(request, 'properties/profile.html')

def logout_page(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('index')