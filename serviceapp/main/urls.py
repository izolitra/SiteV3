from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index_page'),
    path('applications/', views.applications, name='applications_page'),
    path('profile_auto/payment/', views.profile_auto_payment, name='profile_auto_payment'),
    path('profile_auto/create_order/', views.create_order, name='create_order'),
    path('mechanic/<int:mechanic_id>/', views.mechanic_detail, name='mechanic_detail'),
    path('create_order/<int:id>/<int:order_id>/', views.create_order, name='create_order')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)