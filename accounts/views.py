from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import (UserLoginForm, UserRegistrationForm1, UserRegistrationForm2,
                    DoctorRegistrationForm, PatientRegistrationForm)
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import BaseUserManager

from .decorators import doctor_login_required
from .models import MedUser
# Create your views here.


def get_home(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            u = login_form.cleaned_data['username']
            p = login_form.cleaned_data['password']
            user = authenticate(username=u, password=p)

            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                login_form.add_error(None, "Login information is wrong or your account is not active.")
    else:
        login_form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': login_form})


def register_doctor(request):
    if request.method == "POST":
        user_form = UserRegistrationForm1(request.POST)
        doctor_form = DoctorRegistrationForm(request.POST)


        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 1
            user.is_active = False
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            u = user_form.cleaned_data['username']
            p = user_form.cleaned_data['password1']
            user = authenticate(username=u, password=p)

            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                user_form.add_error(None, "Registration completed, Please contact with site admin for activation.")
    else:
        user_form = UserRegistrationForm1()
        doctor_form = DoctorRegistrationForm()

    return render(request, "accounts/register.html", {'user_form': user_form, 'user_type_form': doctor_form})


@doctor_login_required
def register_patient(request):
    if request.method == "POST":
        user_form = UserRegistrationForm2(request.POST)
        patient_form = PatientRegistrationForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 2
            user.username = user.first_name[0] + user.last_name
            pwd = BaseUserManager().make_random_password()
            user.set_password(pwd)
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.creator = MedUser.objects.get(username = request.user)
            patient.save()

            user_form.add_error(None, "Patient registered with username = {} with random password = {}"
                                .format(user.username,pwd))
            # return redirect("/")
    else:
        user_form = UserRegistrationForm2()
        patient_form = PatientRegistrationForm()

    return render(request, "accounts/register.html", {'user_form': user_form, 'user_type_form': patient_form})


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url="/accounts/login")
def profile(request):
    return render(request, "accounts/profile.html")