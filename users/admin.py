
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class MyUserAdmin(BaseUserAdmin):
    ordering = ('email',)  # или другое поле, которое есть в вашей модели!
    list_display = ('email',)  # укажите реальные поля вашей модели
    # любые другие поля и конфигурацию под вашу модель

admin.site.register(User, MyUserAdmin)
