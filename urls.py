from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import redirect

from steamer.webapp import views
from steamer import settings

from django.contrib import admin
admin.autodiscover()

THEME = settings.DJAGIOS_THEME

urlpatterns = patterns('',
    #Admin
    (r'^admin/', admin.site.urls),
    (r'^grappelli/', include('grappelli.urls')),

    #Rest
    (r'^api/', include('steamer.api.urls')),

    #WebApp
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.png'}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': '%s/login.html' % THEME}),
    (r'^logout', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login'},),
    (r'^hosttemplate/add', views.add_host_template),
    (r'^host/add', views.add_host),
    (r'^host/delete', views.delete_host),
    (r'^service/removehost', views.remove_host_from_service),
    #..
    (r'^service/addhost', permission_required('djagios.change_host')(
        TemplateView.as_view(template_name="%s/hostservice.html" % THEME))),
    (r'^json/push$',views.push_and_reload ),
    (r'^$', views.home),
)

