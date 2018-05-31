from django.shortcuts import render
from ...utils import get_user_role, check_admin
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def task_view(request):
    isAdmin = check_admin(get_user_role(request))
    api_name = "view_not_admin"
    if isAdmin:
        api_name = "view"

    if request.method == 'POST':
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})
    else:
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})


@login_required(login_url='login')
def task_create(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    if not isAdmin:
        return render(request, 'workish/views/auth/{}.html'.format(working_on_it), {'error': 'Access Denied!'})

    api_name = 'create'

    if request.method == 'POST':
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})
    else:
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})


@login_required(login_url='login')
def task_request(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    api_name = 'request'

    if request.method == 'POST':
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})
    else:
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})


@login_required(login_url='login')
def task_to_approve(request):
    isAdmin = check_admin(get_user_role(request))
    working_on_it = "working_on_it"
    if isAdmin:
        working_on_it = "working_on_it_admin"

    if not isAdmin:
        return render(request, 'workish/views/auth/{}.html'.format(working_on_it), {'error': 'Access Denied!'})

    api_name = 'to_approve'

    if request.method == 'POST':
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})
    else:
        return render(request, 'workish/views/apis/tasks/{}.html'.format(api_name), {'error': 'Working on it!'})
