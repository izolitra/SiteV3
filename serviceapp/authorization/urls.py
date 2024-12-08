from django.urls import path
from . import views
from .views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', views.profile_view, name="profile"),
    path('login/', views.login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', views.doLogout, name='logout'),
    # path('all-orders/', views.all_orders, name='all_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/take/', views.take_order, name='take_order'),
    path('order/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    path('update-avatar/<int:pk>/', views.update_avatar, name='update_avatar'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
