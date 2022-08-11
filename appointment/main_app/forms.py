from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import *

class admin_reg(UserCreationForm):
	class Meta:
		model = depts
		fields = ['department', 'username', 'password1', 'password2', 'email']

class student_reg(UserCreationForm):
	class Meta:
		model = depts
		fields = ['username', 'password1', 'password2','email']

class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = depts
        fields = ['old_password','new_password1','new_password2']
 