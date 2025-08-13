from django.contrib import admin
from properties.models import Property, Employee
# Register your models here.
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'bedrooms', 'bathrooms', 'area')
    list_filter = ('is_published', 'location')
    search_fields = ('title', 'description')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'email')
    list_editable = ('is_active',)  # Можно включать/выключать прямо в списке