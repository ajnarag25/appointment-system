from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2','email']


class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']
 