from .models import Employees, Roles, Employee_Roles
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def get_user_role(request):
    users = Employees.objects.all().filter(username=request.user.username)
    if len(users) <= 0 or len(users) > 1:
        return render(request, 'workish/views/auth/error_norefresh.html',
                      {'error': 'Something went wrong. Please contact an admin!'})

    user_id = users[0].employee_id
    employee_role = Employee_Roles.objects.all().filter(employee_id=user_id)

    if len(employee_role) <= 0 or len(employee_role) > 1:
        return render(request, 'workish/views/auth/error_norefresh.html',
                      {'error': 'Something went wrong. Please contact an admin!'})

    role_id = employee_role[0].role_id.role_id

    role = Roles.objects.all().filter(role_id=role_id)

    if len(role) <= 0 or len(role) > 1:
        return render(request, 'workish/views/auth/error_norefresh.html',
                      {'error': 'Something went wrong. Please contact an admin!'})
    role = role[0]
    return role

def check_admin(role):
    if role.name == "admin":
        return True
    return False