from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('login_admin', views.login_admin, name="login_admin"),
    path('login_student', views.login_student, name="login_student"),
    path('signup_student', views.signup_student, name="signup_student"),
    path('signup_admin', views.signup_admin, name="signup_admin"),
    path('book_app', views.book_app, name="book_app"),
    path('css_form', views.css_form, name="css_form"),
    path('admin_site', views.admin_site, name="admin_site"),

]