from urllib import request
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
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('login_student')
    
def index(request):
    return render(request, "index.html")

def login_admin(request):
    return render(request, "login_admin.html")

def login_student(request):
    if request.user.is_authenticated:
        return redirect ('book_app_student')
    else:
        if request.method == 'POST':
            userrr = request.POST.get('username')
            passw = request.POST.get('password') 
            request.session['username'] = userrr
            user = authenticate(request, username=userrr,password=passw)
            if user is not None:
                login(request, user)
                return redirect('book_app_student')

            else:
                messages.info(request,'Username/Password is Incorrect')
    
    context = {
    }
    return render(request, "login_student.html", context)

def signup_student(request):
    signup = CreateUserForm()
    if request.method == 'POST':
        signup = CreateUserForm(request.POST)
        if signup.is_valid():
            signup.instance.is_staff = True
            signup.save()
            return redirect('login_student')
        else:
            messages.info(request,'Invalid Credentials!')

    context = {
        'signup': signup,
    }
   
    return render(request, "signup_student.html", context)

def signup_admin(request):
    return render(request, "signup_admin.html")

def book_app(request):
    return render(request, "book_app.html")

@login_required(login_url='login_student')
def book_app_student(request):
    return render(request, "book_app_student.html")

def css_form(request):
    return render(request, "css_form.html")

def logoutStudent(request):
    logout(request)
    return redirect('login_student')


#ADMIN
def admin_site(request):
    return render(request, "admin_site.html")

#SUPERUSER
def dashboard(request):
    return render(request, "dashboard.html")

def create_manage(request):
    return render(request, "create_manage.html")

def appointments(request):
    return render(request, "appointments.html")

def user(request):
    return render(request, "user.html")