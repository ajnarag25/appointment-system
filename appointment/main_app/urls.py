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
    path('signup_admin/', views.signup_admin, name="signup_admin"),
    path('book_app/', views.book_app, name="book_app"),
    path('book_app_student/', views.book_app_student, name="book_app_student"),
    path('css_form/', views.css_form, name="css_form"),
    path('admin_site/', views.admin_site, name="admin_site"),
    path('password/', auth_views.PasswordChangeView.as_view(), name="password"),

]