from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Employees, Roles, Employee_Roles
from ..utils import get_user_role, check_admin


@login_required(login_url='login')
def home(request):
    role = get_user_role(request)
    isAdmin = check_admin(role)
    if isAdmin:
        return render(request, 'workish/views/location_admin.html', {'request': request})
    else:
        return render(request, 'workish/views/location.html', {'request': request})
