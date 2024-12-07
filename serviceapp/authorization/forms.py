from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Mechanic
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate
from django import forms
from .models import Service, Order


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['user', 'category', 'price']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'description']
        labels = {
            'customer_name': 'Имя заказчика',
            'description': 'Описание заказа',
        }


class MechanicAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'login_form__input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'login_form__input'}))


# Форма для регистрации механика
class MechanicRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label="Полное имя")
    username = forms.CharField(max_length=255, required=True, label="Логин")
    phone = forms.CharField(max_length=15, required=True, label="Телефон")
    email = forms.EmailField(required=True, label="Email")

    work_experience = forms.CharField(widget=forms.Textarea, required=False, label="Опыт работы")
    service_category = forms.CharField(max_length=255, required=False, label="Категория услуги")
    service_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Цена услуги")
    car = forms.CharField(max_length=255, required=False, label="Автомобиль")

    class Meta:
        model = User
        fields = (
        'username','email', 'phone', 'full_name', 'password1', 'password2', 'work_experience', 'service_category', 'service_price',
        'car')

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    work_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input'}))
    service_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    service_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-input'}))
    car = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            Mechanic.objects.create(
                user=user,
                work_experience=self.cleaned_data['work_experience'],
                service_category=self.cleaned_data['service_category'],
                service_price=self.cleaned_data['service_price'],
                car=self.cleaned_data['car']
            )
        return user
