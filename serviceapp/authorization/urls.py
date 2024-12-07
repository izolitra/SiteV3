from django.urls import path
from . import views
from .views import register, login_view, profile_view

urlpatterns = [
    path('profile/', views.profile_view, name="profile"),
    path('login/', views.login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', views.doLogout, name='logout'),
    path('dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]