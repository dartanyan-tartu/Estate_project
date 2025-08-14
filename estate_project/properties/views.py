from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login
from .models import Property, Employee
from .forms import RegisterForm


# Главная — список недвижимости с фильтром
# properties/views.py

def index(request):
    properties = Property.objects.filter(is_published=True)

    # Получаем значение фильтра
    bedrooms_filter = request.GET.get('bedrooms')

    # Применяем фильтр
    if bedrooms_filter == 'studio':
        properties = properties.filter(bedrooms=0)  # Студия = 0 комнат
    elif bedrooms_filter == '4+':
        properties = properties.filter(bedrooms__gte=4)  # 4 и более
    elif bedrooms_filter in ['1', '2', '3']:
        properties = properties.filter(bedrooms=int(bedrooms_filter))

    return render(request, 'properties/index.html', {
        'properties': properties,
        'selected': bedrooms_filter,
    })


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


# Профиль
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'properties/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
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