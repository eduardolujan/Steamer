from django.utils.http import urlquote
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME


class DjangoAuthentication(object):
    """Just a Django-authentication provider"""
    def __init__(self, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
        if not login_url:
            login_url = settings.LOGIN_URL
        self.login_url = login_url
        self.redirect_field_name = redirect_field_name
        self.request = None

    def is_authenticated(self, request):
        self.request = request
        return request.user.is_authenticated()

    def challenge(self):
        path = urlquote(self.request.get_full_path())
        tup = self.login_url, self.redirect_field_name, path
        return HttpResponseRedirect('%s?%s=%s' %tup)

