from django.contrib import admin
from .models import Property
from .models import Employee

admin.site.register(Property)
admin.site.register(Employee)