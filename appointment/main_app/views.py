from multiprocessing import context
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

#LOGIN
def login_superuser(request):
    if request.user.is_authenticated:
        return redirect ('dashboard')
    else:
        if request.method == 'POST':
            print('geh lods')
            userrr = request.POST.get('username')
            passw = request.POST.get('password') 
            print(userrr)
            print(passw)
            user = authenticate(request, username=userrr,password=passw)
            if user is not None:
                get_superuser = depts.objects.get(username=userrr)
                if get_superuser.is_superuser == False:
                    messages.info(request,'Something went wrong')
                    return redirect('login_superuser')
                else:
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.info(request,'Username/Password is Incorrect')

    return render(request, "login_superuser.html")

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
                    if dept_names == 'SD':
                        request.session['department'] = departs
                        return redirect('admin_site_sg')
                    elif dept_names == 'RE':
                        request.session['department'] = departs
                        return redirect('admin_site_re')
                    else:
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

#SIGNUP
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

#APPOINTMENTS
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
    get_css_form = formcss(request.POST or None)
    print(get_css_form)
    if request.method == 'POST':
        if get_css_form.is_valid():
            print(get_css_form)
            get_css_form.save()
            messages.info(request,'Successfully Submitted')
            return redirect('css_form')

    return render(request, "css_form.html")


#LOGOUT 
def logoutSuperuser(request):
    logout(request)
    return redirect('login_superuser')

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
    get_compose_msg_2 = request.POST.get('compose_msg_2')
    get_id_approved = request.POST.get('id_accept')
    get_id_declined = request.POST.get('id_decline')
    get_id_delete = request.POST.get('id_delete')
    get_id_compose = request.POST.get('id_compose')
    get_id_compose_2 = request.POST.get('id_compose_2')
    get_id_reapproved = request.POST.get('id_reapproved')

    get_name = request.POST.get('student_name')
    if get_name != None:
        composed_name_header = 'Good day,' + ' ' + get_name
        get_email = request.POST.get('student_email')
        hostemail = 'tupcappointment2022@gmail.com'
        msg = 'We would like you to fill-up our CSS form we already accepted your appointment.' + '\n' + 'Please click the link provided to open the css form' + ' http://127.0.0.1:8000/css_form/' + '\n' + 'Thank you have a nice day.' + '\n \n' + '- TUPC_APPOINTMENT_2022'  
        send_mail(
            composed_name_header,
            msg,
            hostemail,
            [get_email],
        )
        messages.info(request,'Css Form has been sent')

    if get_compose_msg != None:
        get_name = request.POST.get('student_name_3')
        appointmentForm.objects.filter(id = get_id_compose).update(notes=get_compose_msg)
        composed_name_header = 'Good day,' + ' ' + get_name
        get_email = request.POST.get('student_email_3')
        hostemail = 'tupcappointment2022@gmail.com'
        msg = get_compose_msg + '\n \n' + '- TUPC_APPOINTMENT_2022'
        send_mail(
            composed_name_header,
            msg,
            hostemail,
            [get_email],
        )
        messages.info(request,'Message has been sent')
    
    if get_compose_msg_2 != None:
        get_name = request.POST.get('student_name_2')
        appointmentForm.objects.filter(id = get_id_compose_2).update(notes=get_compose_msg_2)
        composed_name_header = 'Good day,' + ' ' + get_name
        get_email = request.POST.get('student_email_2')
        hostemail = 'tupcappointment2022@gmail.com'
        msg = get_compose_msg_2 + '\n \n' + '- TUPC_APPOINTMENT_2022'
        send_mail(
            composed_name_header,
            msg,
            hostemail,
            [get_email],
        )
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

    checkapp3 = appointmentForm.objects.filter(id = get_id_reapproved).update(status='APPROVED')
    if checkapp3 == 1:
        messages.info(request,'Successfully Approved')

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

    context = {
        'dept_name' : set_val,
        'dept_val_1': get_appointment_pending,
        'dept_val_2': get_appointment_approved, 
        'dept_val_3': get_appointment_declined, 
        'dept_val_4': get_appointment_history, 
    }


    return render(request, "admin_site.html", context)

@login_required(login_url='login_admin')
def admin_site_sg(request):
    get_appointment_approved = appointmentForm.objects.filter(status='APPROVED').values()
    get_id_delete = request.POST.get('id_delete')
    print(get_id_delete)
    if get_id_delete != None:
        delete_app = appointmentForm.objects.filter(id=get_id_delete)
        delete_app.delete()
        messages.info(request,'Successfully Deleted!')
        
    get_dept = request.session['department']
    if get_dept == 'SD':
        set_val = 'Security Department'

    context={
        'dept_name': set_val,
        'dept_val_1': get_appointment_approved
    }
    return render(request, "admin_site_sg.html", context)


@login_required(login_url='login_admin')
def admin_site_re(request):
    get_cssform = cssform.objects.all()
    get_dept = request.session['department']
    if get_dept == 'RE':
        set_val = 'Research & Extension'

    context={
        'dept_name': set_val,
        'cssform': get_cssform
    }
    return render(request, "admin_site_re.html", context)

#SUPERUSER
@login_required(login_url='login_superuser')
def dashboard(request):
    get_faculty = depts.objects.filter(is_staff = 0).values()
    get_student = depts.objects.filter(is_staff = 1).values()
    get_appointments = appointmentForm.objects.all()

    store_length_1 = len(get_faculty) 
    save_length_1 = [store_length_1]

    store_length_2 = len(get_student) 
    save_length_2 = [store_length_2]

    store_length_3 = len(get_appointments) 
    save_length_3 = [store_length_3]

    context = {
        'faculty': get_faculty,
        'length1': save_length_1,
        'length2': save_length_2,
        'length3': save_length_3,
    }
    return render(request, "dashboard.html", context)

@login_required(login_url='login_superuser')
def create_manage(request):
    get_faculty = depts.objects.filter(is_staff = 0).values()
    get_student = depts.objects.filter(is_staff = 1).filter(is_superuser = 0).values()
    get_app = appointmentForm.objects.all()

    get_id_update_admin = request.POST.get('id_update_admin')
    if get_id_update_admin != None:
        get_username = request.POST.get('username')
        get_first_name = request.POST.get('first_name')
        get_last_name = request.POST.get('last_name')
        get_email = request.POST.get('email')
        get_department = request.POST.get('department')
        depts.objects.filter(id=get_id_update_admin).update(username=get_username)
        depts.objects.filter(id=get_id_update_admin).update(first_name=get_first_name)
        depts.objects.filter(id=get_id_update_admin).update(last_name=get_last_name)
        depts.objects.filter(id=get_id_update_admin).update(email=get_email)
        depts.objects.filter(id=get_id_update_admin).update(department=get_department)
        messages.info(request,'Successfully Updated')

    get_id_delete_admin = request.POST.get('id_delete_admin')
    if get_id_delete_admin != None:
        delete_admin = depts.objects.filter(id=get_id_delete_admin)
        delete_admin.delete()
        messages.info(request,'Successfully Deleted!')

    get_id_update_student = request.POST.get('id_update_student')
    if get_id_update_student != None:
        get_username = request.POST.get('username')
        get_email = request.POST.get('email')
        depts.objects.filter(id=get_id_update_student).update(username=get_username)
        depts.objects.filter(id=get_id_update_student).update(email=get_email)
        messages.info(request,'Successfully Updated')

    get_id_delete_student = request.POST.get('id_delete_student')
    if get_id_delete_student != None:
        delete_student = depts.objects.filter(id=get_id_delete_student)
        delete_student.delete()
        messages.info(request,'Successfully Deleted!')

    signup_admin = admin_reg()
    if request.method == 'POST':
        signup_admin = admin_reg(request.POST)
        if signup_admin.is_valid():
            signup_admin.save()
            messages.info(request,'Successfully Created Admin Account!')
            return redirect('create_manage')

    context = {
        'signup_admin': signup_admin,
        'faculty': get_faculty,
        'student': get_student,
        'get_date': get_app
    }
    return render(request, "create_manage.html", context)

@login_required(login_url='login_superuser')
def appointments(request):
    get_appointment_pending = appointmentForm.objects.filter(status='PENDING').values()
    get_appointment_approved = appointmentForm.objects.filter(status='APPROVED').values()
    get_appointment_declined = appointmentForm.objects.filter(status='DECLINED').values()
    get_appointment_history = appointmentForm.objects.all()
    get_css_form = cssform.objects.all()

    store_length_pending = len(get_appointment_pending)
    save_length_pending = [store_length_pending]

    store_length_approved = len(get_appointment_approved)
    save_length_approved = [store_length_approved]

    store_length_decline = len(get_appointment_declined)
    save_length_decline = [store_length_decline]

    store_length_cssform = len(get_css_form)
    save_length_cssform = [store_length_cssform]


    context = {
        'get_length_pending': save_length_pending,
        'get_length_approved': save_length_approved,
        'get_length_declined': save_length_decline,
        'get_length_cssform': save_length_cssform,
        'dept_val': get_appointment_history, 
        'css_form_data': get_css_form
    }
    return render(request, "appointments.html", context)

@login_required(login_url='login_superuser')
def user(request):
    superuser = depts.objects.filter(is_superuser = True).values()
    get_id_superuser = request.POST.get('id_superuser')

    if get_id_superuser is not None:
        get_username = request.POST.get('username')
        get_first_name = request.POST.get('first_name')
        get_last_name = request.POST.get('last_name')
        get_email = request.POST.get('email')
        depts.objects.filter(id=get_id_superuser).update(username=get_username)
        depts.objects.filter(id=get_id_superuser).update(first_name=get_first_name)
        depts.objects.filter(id=get_id_superuser).update(last_name=get_last_name)
        depts.objects.filter(id=get_id_superuser).update(email=get_email)
        messages.info(request,'Successfully Updated')

    context = {
        'get_superuser': superuser
    }
    return render(request, "user.html", context)