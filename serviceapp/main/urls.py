from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index_page'),
    path('applications/', views.applications, name='applications_page'),
]