
from django.urls import path
from .views import LoginView,register_customer,CombinedUpdateView,manage_phone_numbers,delete_phone_number
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, reverse_lazy


urlpatterns = [
path('تسجيل الدخول/', LoginView.as_view(), name='login'),
path('إنشاء حساب/', register_customer, name='register_view'),
path('profile/', CombinedUpdateView.as_view(), name='profile'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path(
        'change_password/',
        PasswordChangeView.as_view(
            template_name='change_password.html',
            success_url=reverse_lazy('home'),
        ),
        name='change_password'
    ),
path('manage_phone_numbers/', manage_phone_numbers, name='manage_phone_numbers'),
path('delete_phone_number/<int:pk>/', delete_phone_number, name='delete_phone_number'),





]
