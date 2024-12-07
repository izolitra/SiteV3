from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_auto_home, name='profile_auto_home'),
    path('payment/', views.profile_auto_payment, name='payment')
]