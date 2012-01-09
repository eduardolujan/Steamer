from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import redirect

from doctor.webapp import views
from doctor import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    #Admin
    (r'^admin/', admin.site.urls),
    (r'^grappelli/', include('grappelli.urls')),

    #Rest
    (r'^api/', include('doctor.api.urls')),

    #WebApp
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.png'}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': '%s/login.html'%settings.DJAGIOS_THEME}),
    (r'^logout', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login'},),
    (r'^hosttemplate/add', views.add_host_template),
    (r'^host/add', views.add_host),
    (r'^host/delete', views.delete_host),
    (r'^service/addhost', views.add_host_to_service),
    (r'^service/removehost', views.remove_host_from_service),
    (r'^json/push$',views.push_and_reload ),
    (r'^$', views.home),
)

