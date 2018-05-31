from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
#from images.views import home
from workish.views import home as home_old
from workish.all_views.home import home
from workish.all_views.session import clogin, clogout, csignup
from workish.all_views.admin_stuff import main_gba, init_gba

from workish.all_views.apis.tasks import task_view, task_create, task_request, task_to_approve
from workish.all_views.apis.teams import teams_view, teams_create
from workish.all_views.apis.users import users_view, users_create
from workish.all_views.apis.roles import roles_view, roles_create


urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^gba/main_gba', main_gba, name='main_gba'),
    url(r'^gba/init', init_gba, name='main_gba'),
    #url(r'^home_old$', home_old, name='home'),
    url(r'^home$', home, name='home'),
    url(r'^login', clogin, name='login'),
    url(r'^logout', clogout, name='logout'),
    url(r'^signup', csignup, name='signup'),

    url(r'^tasks/view', task_view, name='task_view'),
    url(r'^tasks/create', task_create, name='task_create'),
    url(r'^tasks/request', task_request, name='task_request'),
    url(r'^tasks/toapprove', task_to_approve, name='task_to_approve'),

    url(r'^teams/view', teams_view, name='teams_view'),
    url(r'^teams/create', teams_create, name='teams_create'),

    url(r'^users/view', users_view, name='users_view'),
    url(r'^users/create', users_create, name='users_create'),

    url(r'^roles/view', roles_view, name='roles_view'),
    url(r'^roles/create', roles_create, name='roles_create'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
