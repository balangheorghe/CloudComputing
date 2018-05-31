from django.shortcuts import render
from ...utils import get_user_role, check_admin
from django.contrib.auth.decorators import login_required
from ...models import Employees, Roles, Employee_Roles
from django.contrib.auth.models import User

@login_required(login_url='login')
def users_view(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    api_name = 'view'

    if not isAdmin:
        return render(request, 'workish/views/auth/{}.html'.format(working_on_it), {'error': 'Access Denied!'})

    rt = Employees.objects.all()
    return render(request, 'workish/views/apis/users/{}.html'.format(api_name), {'user_list': rt})


@login_required(login_url='login')
def users_create(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    api_name = 'create'

    if not isAdmin:
        return render(request, 'workish/views/auth/{}.html'.format(working_on_it), {'error': 'Access Denied!'})

    if request.method == 'POST':
        sfirstname = request.POST.get('firstname', '')
        slastname = request.POST.get('lastname', '')
        susername = request.POST.get('username', '')
        scnp = request.POST.get('cnp', '')
        semail = request.POST.get('email', '')
        scellphone = request.POST.get('cellphone', '')
        spassword = request.POST.get('password', '')
        srepassword = request.POST.get('repassword', '')
        slinemanager = request.POST.get('linemanager', '')
        srole = request.POST.get('role', '')

        if sfirstname == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'First Name not provided!'})

        if slastname == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Last Name not provided!'})

        if susername == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Username not provided!'})

        if scnp == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'CNP not provided!'})
        elif len(scnp) != 13:
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'CNP is not valid!'})

        if semail == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Address not provided!'})

        if scellphone == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Cellphone not provided!'})

        if spassword == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Password not provided!'})

        if srepassword == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'RePassword not provided!'})

        if spassword != srepassword:
            return render(request, 'workish/views/auth/error.html',
                          {'error': 'Password and RePassword are not the same!'})

        if srole == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Role not provided!'})

        rt = User.objects.all().filter(username=susername)
        if len(rt) > 0:
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'User already exists'})

        user = User.objects.create_user(username=susername, email=semail, password=spassword)
        user.save()

        if slinemanager == '':
            slinemanager = None
        else:
            line_manager = Employees.objects.all().filter(username=slinemanager)
            if len(line_manager) <= 0 or len(line_manager) > 1:
                return render(request, 'workish/views/apis/error_admin.html',
                              {'error': 'Something went wrong. Please contact an admin! Error: Invalid line manager'})
            slinemanager = Employees.objects.get(username=slinemanager)

        employee = Employees(first_name=sfirstname, last_name=slastname,
                             cnp=scnp, email=semail, cellphone=scellphone,
                             username=susername, line_manager=slinemanager)
        employee.save()

        role_id = Roles.objects.all().filter(name=srole)
        if len(role_id) <= 0 or len(role_id) > 1:
            return render(request, 'workish/views/apis/error_admin.html',
                          {'error': 'Something went wrong. Please contact an admin! Error: Multiple roles'})

        role_id = Roles.objects.get(name=srole)

        employee_id = Employees.objects.all().filter(username=susername)
        if len(employee_id) <= 0 or len(employee_id) > 1:
            return render(request, 'workish/views/apis/error_admin.html',
                          {'error': 'Something went wrong. Please contact an admin!'})

        employee_id = Employees.objects.get(username=susername)

        new_employee_role = Employee_Roles(employee_id=employee_id, role_id=role_id)
        new_employee_role.save()

        return render(request, 'workish/views/apis/success_admin.html'.format(api_name), {'text': 'Successfully signed up.'})

    else:
        return render(request, 'workish/views/apis/users/{}.html'.format(api_name), {'error': 'Working on it!'})
