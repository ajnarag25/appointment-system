from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def login_admin(request):
    return render(request, "login_admin.html")

def login_student(request):
    return render(request, "login_student.html")

def signup_student(request):
    return render(request, "signup_student.html")

def signup_admin(request):
    return render(request, "signup_admin.html")

def book_app(request):
    return render(request, "book_app.html")

def css_form(request):
    return render(request, "css_form.html")

def admin_site(request):
    return render(request, "admin_site.html")