from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Employees, Roles, Employee_Roles
from django.contrib.auth.models import User


def main_gba(request):
    """
    r1 = Roles(name="admin", description="management", type="adminv1")
    r1.save()
    r2 = Roles(name="user", description="management", type="adminv1")
    r2.save()
    """

    User.objects.all().delete()
    Employees.objects.all().delete()
    Employee_Roles.objects.all().delete()

    return render(request, 'workish/views/auth/error_norefresh.html',
                  {'error': 'GBA MODE ACTIVATED. Please contact gba!'})


def init_gba(request):
    r1 = Roles(name="admin", description="management", type="adminv1")
    r1.save()
    r2 = Roles(name="user", description="management", type="adminv1")
    r2.save()
    return render(request, 'workish/views/auth/error_norefresh.html',
                  {'error': 'GBA MODE ACTIVATED. Please contact gba!'})
