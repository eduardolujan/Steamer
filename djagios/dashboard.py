
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class DocDashboard(Dashboard):
    """
    Custom index dashboard for Nagi-o-matic
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Administration & Applications'),
            column=1,
            collapsible=False,
            children = [
                modules.AppList(
                    _('Nagios Config'),
                    column=1,
                    css_classes=('collapse open',),
                    models=('steamer.djagios.*',)
                )
            ]
        ))
        
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            exclude=('steamer.djagios.*','django.contrib.auth.*',),
        ))
        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Auth'),
            column=1,
            collapsible=False,
            models=('django.contrib.auth.*',),
        ))
        
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Links'),
            column=3,
            children=[
                { 'title': _('Quick tool'), 'url': '/', 'external': False, },
                {
                    'title': _('Nagi-o-matic Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Nagios documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Intranet sistemes'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Merlind'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Arquitectura'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=10,
            collapsible=False,
            column=2,
        ))


