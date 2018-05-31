from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.conf import settings
from .models import ADR_GBA as custom_db
from .models import Tasks
from .models import Teams
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        p1 = custom_db(name='{}'.format(request.POST.get("name", "")),
                       address='{}'.format(request.POST.get("address", "")),
                       img='{}'.format(request.POST.get("img", "")))
        p1.save()
        top_list = custom_db.objects.all()
        return render(request, 'workish/home.html',
                              {'data': top_list})
    else:
        tt = ''
        all_users = None
        if request.user.is_authenticated:
            tt = 'auth'
            all_users = User.objects.all()
        else:
            tt = 'noauth'

        top_list = custom_db.objects.all()
        #return render(request, 'workish/home.html', {'data': top_list, 'tt':tt, 'all_users':all_users})
        return render(request, 'workish/views/location.html', {'request':request})