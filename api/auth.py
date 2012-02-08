from django.utils.http import urlquote
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

class MultiAuthentication(object):
        """ Authenticated Django-Piston against multiple types of authentication,
        it used to be https://gist.github.com/790222 """


        def __init__(self, auth_types):
            """ Takes a list of authenication objects to try against, the default
            authentication type to try is the first in the list. """
            self.auth_types = auth_types
            self.selected_auth = auth_types[0]

        def is_authenticated(self, request):
            """ Try each authentication type in order and use the first that succeeds """
            authenticated = False
            for auth in self.auth_types:
                authenticated = auth.is_authenticated(request)
                if authenticated:
                    selected_auth = auth
                    break
            return authenticated

        def challenge(self):
            """ Return the challenge for whatever the selected auth type is (or the default 
            auth type which is the first in the list)"""
            return self.selected_auth.challenge()


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

