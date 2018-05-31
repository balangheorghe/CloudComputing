from django.shortcuts import render
from ...utils import get_user_role, check_admin
from django.contrib.auth.decorators import login_required
from ...models import Team_Assignments, Teams, Employees

@login_required(login_url='login')
def teams_view(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    api_name = 'view_not_admin'
    if isAdmin:
        api_name = 'view'
        working_on_it = "working_on_it_admin"

    if isAdmin:
        rt = Teams.objects.all()
    else:
        emp = Employees.objects.get(username=request.user.username)
        rt = Team_Assignments.objects.all().filter(employee_id=emp)
    return render(request, 'workish/views/apis/teams/{}.html'.format(api_name), {'team_list': rt})


@login_required(login_url='login')
def teams_create(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    if not isAdmin:
        return render(request, 'workish/views/auth/{}.html'.format(working_on_it), {'error': 'Access Denied!'})

    api_name = 'create'

    if request.method == 'POST':
        sname = request.POST.get('name', '')
        sleader = request.POST.get('leader', '')
        sspecific = request.POST.get('specific', '')
        slocation = request.POST.get('location', '')

        if sname == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Name not provided!'})

        if sleader == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Leader not provided!'})

        if sspecific == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Specific not provided!'})

        if slocation == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Location not provided!'})

        tt = Employees.objects.all().filter(username=sleader)
        if len(tt) <= 0 or len(tt) > 1:
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Leader username not found'})

        employees = Employees.objects.get(username=sleader)

        t1 = Teams(name=sname, specific=sspecific, base_location=slocation, leader_id=employees)
        t1.save()

        api_name = 'success'

        return render(request, 'workish/views/apis/{}.html'.format(api_name), {'error': 'Working on it!'})
    else:
        return render(request, 'workish/views/apis/teams/{}.html'.format(api_name), {'error': 'Working on it!'})
