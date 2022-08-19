from tkinter.messagebox import NO
from tkinter.tix import STATUS
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
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

# Create your views here.
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('login_student')
    
def index(request):
    return render(request, "index.html")

def login_admin(request):
    if request.user.is_authenticated:
        return redirect ('admin_site')
    else:
        if request.method == 'POST':
            userrr = request.POST.get('username')
            passw = request.POST.get('password') 
            dept_names = request.POST.get('department')
            user = authenticate(request, username=userrr,password=passw)
            if user is not None:
                get_dept = depts.objects.get(username=userrr)
                departs = get_dept.department
                print(get_dept)
                if get_dept.department == "":
                    messages.info(request,'Something went wrong')
                    return redirect('login_admin')
                elif dept_names != get_dept.department:
                    messages.info(request,'Your Account is not in the right Department')
                    return redirect('login_admin')
                else:
                    login(request, user)
                    request.session['username'] = userrr
                    request.session['department'] = departs
                    return redirect('admin_site')

            else:
                messages.info(request,'Username/Password is Incorrect')
    
    context = {
    }
    return render(request, "login_admin.html", context)

def login_student(request):
    if request.user.is_authenticated:
        return redirect ('book_app_student')
    else:
        if request.method == 'POST':
            userrr = request.POST.get('username')
            passw = request.POST.get('password') 
            # check_pass = depts.objects.filter(username = userrr).values()
            # print(check_pass)
            # for p in check_pass:
            #     checkpass = p['password']
            #     print(checkpass)
            #     matchcheck= check_password(passw, checkpass)
            #     print(matchcheck)
            user = authenticate(request, username=userrr,password=passw)
            if user is not None:
                get_staff = depts.objects.get(username=userrr)
                if get_staff.is_staff == False:
                    messages.info(request,'Something went wrong')
                    return redirect('login_student')
                else:
                    login(request, user)
                    request.session['username_student'] = userrr
                    return redirect('book_app_student')

            else:
                messages.info(request,'Username/Password is Incorrect')
    
    context = {
    }
    return render(request, "login_student.html", context)

def signup_student(request):
    signup = student_reg()
    if request.method == 'POST':
        signup = student_reg(request.POST)
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


def book_app(request):
    get_data = depts.objects.filter(is_staff = 0).values()
    get_appointment = appointmentGuest(request.POST or None)
    if request.method == 'POST':
        if get_appointment.is_valid():
            print(get_appointment)
            get_appointment.save()
            messages.info(request,'Successfully Submitted')
            return redirect('book_app')

    context = {
        'names': get_data
    }
    return render(request, "book_app.html", context)

@login_required(login_url='login_student')
def book_app_student(request):
    get_user = request.session['username_student']
    get_form_user = appointmentForm.objects.filter(username = get_user)
    get_data = depts.objects.filter(is_staff = 0).values()
    get_appointment = appointmentGuest(request.POST or None)

    store_form_user_data = []
    for x in get_form_user:
        store_form_user_data.append(x)

    if request.method == 'POST':
        if get_appointment.is_valid():
            print(get_appointment)
            get_appointment.save()
            messages.info(request,'Successfully Submitted')
            return redirect('book_app_student')

    context = {
        'names': get_data,
        'username': get_user,
        'get_user_data': store_form_user_data
    }
    return render(request, "book_app_student.html", context)


@login_required(login_url='login_student')
def book_app_alumni(request):
    get_user = request.session['username_student']
    get_form_user = appointmentForm.objects.filter(username = get_user)
    get_data = depts.objects.filter(is_staff = 0).values()
    get_appointment = appointmentGuest(request.POST or None)

    store_form_user_data = []
    for x in get_form_user:
        store_form_user_data.append(x)

    if request.method == 'POST':
        if get_appointment.is_valid():
            print(get_appointment)
            get_appointment.save()
            messages.info(request,'Successfully Submitted')
            return redirect('book_app_alumni')

    context = {
        'names': get_data,
        'username': get_user,
        'get_user_data': store_form_user_data
    }
    return render(request, "book_app_alumni.html", context)


def css_form(request):
    return render(request, "css_form.html")


#LOGOUT 
def logoutAdmin(request):
    logout(request)
    return redirect('login_admin')

def logoutStudent(request):
    logout(request)
    return redirect('login_student')


#ADMIN
@login_required(login_url='login_admin')
def admin_site(request):
    get_dept = request.session['department']
    get_compose_msg = request.POST.get('compose_msg')
    get_id_approved = request.POST.get('id_accept')
    get_id_declined = request.POST.get('id_decline')
    get_id_delete = request.POST.get('id_delete')
    get_id_compose = request.POST.get('id_compose')

    get_name = request.POST.get('student_name')
    if get_name != None:
        composed_name_header = 'Good day,' + ' ' + get_name
        get_email = request.POST.get('student_email')
        hostemail = 'tupcappointment2022@gmail.com'
        msg = 'We would like you to fill-up our CSS form we already accepted your appointment.' + ' ' + 'Please click the link provided to open the css form' + ' http://127.0.0.1:8000/css_form/' + ' ' + 'Thank you have a nice day.'  
        send_mail(
            composed_name_header,
            msg,
            hostemail,
            [get_email],
        )
        messages.info(request,'Css Form has been sent')
        
    if get_compose_msg != None:
        appointmentForm.objects.filter(id = get_id_compose).update(notes=get_compose_msg)
        messages.info(request,'Message has been sent')

    if get_id_delete != None:
        delete_app = appointmentForm.objects.filter(id=get_id_delete)
        delete_app.delete()
        messages.info(request,'Successfully Deleted!')

    checkapp1 = appointmentForm.objects.filter(id = get_id_approved).update(status='APPROVED')
    if checkapp1 == 1:
        messages.info(request,'Successfully Approved')

    checkapp2 = appointmentForm.objects.filter(id = get_id_declined).update(status='DECLINED')
    if checkapp2 == 1:
        messages.info(request,'Successfully Declined')


    get_appointment_pending = appointmentForm.objects.filter(dept = get_dept).filter(status='PENDING').values()
    get_appointment_approved = appointmentForm.objects.filter(dept = get_dept).filter(status='APPROVED').values()
    get_appointment_declined = appointmentForm.objects.filter(dept = get_dept).filter(status='DECLINED').values()
    get_appointment_history = appointmentForm.objects.filter(dept = get_dept).values()

    if get_dept == "OAA":
        set_val = 'Office of Academic Affair'
    elif get_dept == "DIT":
        set_val = 'Department of Information Technology'
    elif get_dept == "DLA":
        set_val = 'Department of Liberal Arts'
    elif get_dept == "OCL":
        set_val = 'Office of Campus Library'
    elif get_dept == "ORE":
        set_val = 'Office of Research and Extension'
    elif get_dept == "DMS":
        set_val = 'Department of Mathematics and Science'
    elif get_dept == "DOE":
        set_val = 'Department of Engineering'
    elif get_dept == "OSA":
        set_val = 'Office of Student Affairs'
    elif get_dept == "UITC":
        set_val = 'University Information Technology Center '
    elif get_dept == "DPE":
        set_val = 'Department of Physical Education'
    elif get_dept == "SD":
        set_val = 'Security Department'

    context = {
        'dept_name' : set_val,
        'dept_val_1': get_appointment_pending,
        'dept_val_2': get_appointment_approved, 
        'dept_val_3': get_appointment_declined, 
        'dept_val_4': get_appointment_history, 
    }


    return render(request, "admin_site.html", context)

#SUPERUSER
def dashboard(request):
    return render(request, "dashboard.html")

def create_manage(request):
    signup_admin = admin_reg()
    if request.method == 'POST':
        signup_admin = admin_reg(request.POST)
        print(signup_admin)
        if signup_admin.is_valid():
            signup_admin.save()
            messages.info(request,'Successfully Created Admin Account!')
            return redirect('create_manage')

    context = {
        'signup_admin': signup_admin,
    }
    return render(request, "create_manage.html", context)

def appointments(request):
    return render(request, "appointments.html")

def user(request):
    return render(request, "user.html")