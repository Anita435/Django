from django.urls import path,re_path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_base, name='dashboard_base'),
    path('fill/otp', views.fill_data, name='fill_data'),
    path('reset/password', views.password_reset, name='password_reset'),
    path('sent/otp', views.sent_otp, name='sent_otp'),
    path('verify/otp', views.verify_otp, name='verify_otp'),
    path('change/password', views.change_password, name='fill_password'),
    path('change-password-inner/', views.change_password_inner, name='change_password'),
    path('users/', views.all_user, name='all_user'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
