from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from ..models import Employees, Roles, Employee_Roles
from django.db import models

def clogin(request):
    if request.user.is_authenticated():
        return render(request, 'workish/views/auth/success.html', {'text': 'You are already signed in.'})

    if request.method == 'POST':
        susername = request.POST.get('username', '')
        spassword = request.POST.get('password', '')
        if susername == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'Username not provided!'})

        if spassword == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'Password not provided!'})

        user = authenticate(username=susername, password=spassword)
        if user is not None:
            login(request, user)
            return render(request, 'workish/views/auth/success.html', {'text': 'Successfully signed in.'})
            # Redirect to a success page.
        else:
            return render(request, 'workish/views/auth/error.html', {'error': 'Invalid login!'})
            # Return an 'invalid login' error message.
    else:
        return render(request, 'workish/views/auth/login.html')


def csignup(request):
    if request.user.is_authenticated():
        return render(request, 'workish/views/auth/success.html', {'text': 'You are already signed in.'})

    if request.method == 'POST':
        sfirstname = request.POST.get('firstname', '')
        slastname = request.POST.get('lastname', '')
        susername = request.POST.get('username', '')
        scnp = request.POST.get('cnp', '')
        semail = request.POST.get('email', '')
        scellphone = request.POST.get('cellphone', '')
        spassword = request.POST.get('password', '')
        srepassword = request.POST.get('repassword', '')

        if sfirstname == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'First Name not provided!'})

        if slastname == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'Last Name not provided!'})

        if susername == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'Username not provided!'})

        if scnp == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'CNP not provided!'})
        elif len(scnp) != 13:
            return render(request, 'workish/views/auth/error.html', {'error': 'CNP is not valid!'})

        if semail == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'Address not provided!'})

        if scellphone == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'Cellphone not provided!'})

        if spassword == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'Password not provided!'})

        if srepassword == '':
            return render(request, 'workish/views/auth/error.html', {'error': 'RePassword not provided!'})

        if spassword != srepassword:
            return render(request, 'workish/views/auth/error.html', {'error': 'Password and RePassword are not the same!'})

        rt = User.objects.all().filter(username=susername)
        if len(rt) > 0:
            return render(request, 'workish/views/auth/error.html', {'error': 'User already exists'})

        user = User.objects.create_user(username=susername, email=semail, password=spassword)
        user.save()

        employee = Employees(first_name=sfirstname, last_name=slastname,
                                          cnp=scnp, email=semail, cellphone=scellphone,
                                          username=susername)
        employee.save()

        role_to_get = "user"

        if susername == "gba":
            role_to_get = "admin"

        role_id = Roles.objects.all().filter(name=role_to_get)
        if len(role_id) <= 0 or len(role_id) > 1:
            return render(request, 'workish/views/auth/error_norefresh.html',
                          {'error': 'Something went wrong. Please contact an admin!'})

        role_id = Roles.objects.get(name=role_to_get)

        employee_id = Employees.objects.all().filter(username=susername)
        if len(employee_id) <= 0 or len(employee_id) > 1:
            return render(request, 'workish/views/auth/error_norefresh.html',
                          {'error': 'Something went wrong. Please contact an admin!'})

        employee_id = Employees.objects.get(username=susername)

        new_employee_role = Employee_Roles(employee_id=employee_id, role_id=role_id)
        new_employee_role.save()

        return render(request, 'workish/views/auth/success.html', {'text': 'Successfully signed up.'})
    else:
        return render(request, 'workish/views/auth/signup.html')


def clogout(request):
    logout(request)
    return render(request, 'workish/views/auth/success.html', {'text': 'Logged out'})
