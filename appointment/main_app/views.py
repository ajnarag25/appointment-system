from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


# Create your views here.
def change_password(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('login_student')
    
def index(request):
    return render(request, "index.html")

def login_admin(request):
    return render(request, "login_admin.html")

def login_student(request):
    return render(request, "login_student.html")

def signup_student(request):
    signup = CreateUserForm()
    if request.method == 'POST':
        signup = CreateUserForm(request.POST)
        messages.info(request,'Something went wrong!')
        if signup.is_valid():
            signup.save()
            return redirect('login_student')

    context = {
        'signup': signup,
    }
   
    return render(request, "signup_student.html", context)

def signup_admin(request):
    return render(request, "signup_admin.html")

def book_app(request):
    return render(request, "book_app.html")

def book_app_student(request):
    return render(request, "book_app_student.html")

def css_form(request):
    return render(request, "css_form.html")

def admin_site(request):
    return render(request, "admin_site.html")

