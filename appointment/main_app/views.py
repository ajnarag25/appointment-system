from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "index.html")

def login_admin(request):
    return render(request, "login_admin.html")

def login_student(request):
    return render(request, "login_student.html")

def signup_student(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        messages.info(request,'Something went wrong!')
        if form.is_valid():
            messages.info(request,'Successfully Registered your Account!')
            form.save()
            return redirect('login_student')

    context = {
        'form': form
    }
   
    return render(request, "signup_student.html", context)

def signup_admin(request):
    return render(request, "signup_admin.html")

def book_app(request):
    return render(request, "book_app.html")

def css_form(request):
    return render(request, "css_form.html")

def admin_site(request):
    return render(request, "admin_site.html")