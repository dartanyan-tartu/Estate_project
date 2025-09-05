# properties/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login
from django.db.models import Q
from .models import Property, Employee, Profile
from .forms import RegisterForm


# Главная — с фильтрами и сортировкой
class PropertyListView(ListView):
    model = Property
    template_name = 'properties/index.html'
    context_object_name = 'properties'
    paginate_by = 6

    def get_queryset(self):
        queryset = Property.objects.filter(is_published=True)

        # Фильтр по комнатам
        bedrooms = self.request.GET.get('bedrooms')
        if bedrooms == 'studio':
            queryset = queryset.filter(bedrooms=0)
        elif bedrooms in ['1', '2', '3']:
            queryset = queryset.filter(bedrooms=int(bedrooms))

        # Фильтр по площади
        area = self.request.GET.get('area')
        if area == 'small':
            queryset = queryset.filter(area__lt=50)
        elif area == 'medium':
            queryset = queryset.filter(area__gte=50, area__lt=90)
        elif area == 'large':
            queryset = queryset.filter(area__gte=90)

        # Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'area_asc':  # Новое: по возрастанию
            queryset = queryset.order_by('area')
        elif sort == 'area_desc':
            queryset = queryset.order_by('-area')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_bedrooms'] = self.request.GET.get('bedrooms')
        context['selected_area'] = self.request.GET.get('area')
        context['selected_sort'] = self.request.GET.get('sort')
        return context


# Детали недвижимости
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'
    pk_url_kwarg = 'prop_id'

    def get_queryset(self):
        return Property.objects.filter(is_published=True)


# Сотрудники
class TeamView(ListView):
    model = Employee
    template_name = 'properties/team.html'
    context_object_name = 'employees'
    queryset = Employee.objects.filter(is_active=True).order_by('created_at')


# О нас
class AboutView(TemplateView):
    template_name = 'properties/about.html'


# Профиль
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'properties/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        return context


# Вход
class LoginUserView(LoginView):
    template_name = 'properties/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


# Выход
class LogoutUserView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


# Регистрация
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'properties/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
            return render(request, 'properties/register.html', {'form': form})