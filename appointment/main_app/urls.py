from re import template
from django.urls import path
from .views import PasswordsChangeView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="Home"),
    path('login_admin/', views.login_admin, name="login_admin"),
    path('login_student/', views.login_student, name="login_student"),
    path('signup_student/', views.signup_student, name="signup_student"),
    path('book_app/', views.book_app, name="book_app"),
    path('book_app_student/', views.book_app_student, name="book_app_student"),
    path('book_app_alumni/', views.book_app_alumni, name="book_app_alumni"),
    path('css_form/', views.css_form, name="css_form"),
    path('admin_site/', views.admin_site, name="admin_site"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create_manage/', views.create_manage, name="create_manage"),
    path('appointments/', views.appointments, name="appointments"),
    path('user/', views.user, name="user"),
    path('password/', PasswordsChangeView.as_view(template_name='change-password.html'), name="password"),
    path('logout_student/', views.logoutStudent, name="logout_student"),
    path('logout_admin/', views.logoutAdmin, name="logout_admin"),

]