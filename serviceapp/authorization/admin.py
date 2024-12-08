from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Mechanic, Order

# Определяем ServiceInline перед использованием
class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    fields = ['category', 'price']
    readonly_fields = ['category', 'price']

# Определяем OrderInline перед использованием
class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    fields = ['customer_name', 'description', 'status']
    readonly_fields = ['customer_name', 'description', 'status']
    show_change_link = True  # Добавляет ссылку для перехода на изменение заказа

class MechanicAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'full_name', 'phone', 'email', 'work_experience', 'car', 'avatar_thumbnail'
    )
    search_fields = ['user__username', 'full_name', 'email', 'phone']
    list_editable = ('full_name', 'phone', 'email', 'work_experience', 'car')
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'phone', 'email', 'work_experience', 'car', 'avatar')
        }),
    )
    inlines = [ServiceInline, OrderInline]  # Добавляем отображение заказов

    # Метод для отображения аватара в списке
    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" />', obj.avatar.url)
        return "Нет аватара"
    avatar_thumbnail.short_description = 'Аватар'

# Регистрация моделей
admin.site.register(Mechanic, MechanicAdmin)
admin.site.register(Order)  # Регистрация модели Order
