from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.first)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category} - {self.price}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнен'),
    ]

    mechanic = models.ForeignKey('Mechanic', on_delete=models.SET_NULL, null=True, related_name='orders')
    customer_name = models.CharField(max_length=255, verbose_name="Имя заказчика")
    description = models.TextField(verbose_name="Описание заказа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Заказ от {self.customer_name} ({self.get_status_display()})"

# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    discount = models.IntegerField(default=0, verbose_name="Персональная скидка")

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

# Сигналы для создания и сохранения профиля
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Mechanic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, verbose_name="Полное имя", blank=True)
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True)
    email = models.EmailField(verbose_name="Электронная почта", blank=True)
    work_experience = models.TextField(verbose_name="Опыт работы", blank=True)
    service_category = models.CharField(max_length=255, verbose_name="Категория услуги", blank=True)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена услуги", default=0)
    car = models.CharField(max_length=255, verbose_name="Автомобиль", blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Механик"
        verbose_name_plural = "Механики"