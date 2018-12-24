from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import MedUser, Doctor, Patient
import datetime

now = datetime.datetime.now()


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = MedUser
        fields = ['username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if MedUser.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError('Email addresses must be unique.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Password must not be empty")

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        return password2


class DoctorRegistrationForm(ModelForm):
    class Meta:
        model = Doctor
        fields = []


class PatientRegistrationForm(ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1919, now.year+1)))
    class Meta:
        model = Patient
        fields= ['birth_date']