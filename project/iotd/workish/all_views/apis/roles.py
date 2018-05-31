from django.shortcuts import render
from ...utils import get_user_role, check_admin
from django.contrib.auth.decorators import login_required
from ...models import Roles

@login_required(login_url='login')
def roles_view(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    api_name = 'view'
    rt = Roles.objects.all()
    return render(request, 'workish/views/apis/roles/{}.html'.format(api_name), {'roles_list': rt})


@login_required(login_url='login')
def roles_create(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    if not isAdmin:
        return render(request, 'workish/views/auth/{}.html'.format(working_on_it), {'error': 'Access Denied!'})

    api_name = 'create'

    if request.method == 'POST':
        sname = request.POST.get('name', '')
        sdescription = request.POST.get('description', '')
        stype = request.POST.get('type', '')

        if sname == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Name not provided!'})

        if sdescription == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Sdescription not provided!'})

        if stype == '':
            return render(request, 'workish/views/apis/error_admin.html', {'error': 'Stype not provided!'})

        r1 = Roles(name=sname, description=sdescription, type=stype)
        r1.save()

        api_name = 'success'

        return render(request, 'workish/views/apis/{}.html'.format(api_name), {'error': 'Working on it!'})
    else:
        return render(request, 'workish/views/apis/roles/{}.html'.format(api_name), {'error': 'Working on it!'})
