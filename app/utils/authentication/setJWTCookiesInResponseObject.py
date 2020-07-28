"""Set JWT cookies in response object

    This class take tokens and a response instace for generate cookies with JWT authorization
"""

# Django imports
from django.conf import settings
import datetime


class SetJWTCookiesInResponseObject():

    def __init__(self, access_max_age=None, access_expires=None, refresh_max_age=None, refresh_expires=None):
        """Initial data for cookie

            (max_age): must be int milliseconds .
            (expires): must be timedelta for make a plus with datetime.now().
        """
        self.access_max_age = access_max_age
        self.access_expires = access_expires
        self.refresh_max_age = refresh_max_age
        self.refresh_expires = refresh_expires

    def generate(self, tokens_dict, response_object):
        # General cookie token metadata
        cookie_directives = {
            'secure': settings.COOKIES_SETTING['secure'],
            'httponly': settings.COOKIES_SETTING['http_only']
        }

        access_cookie_directives = self.generate_specific_cookie_directives('access')
        refresh_cookie_directives = self.generate_specific_cookie_directives('refresh')

        response_object.set_cookie(
            'access_token',
            tokens_dict['access'],
            **cookie_directives,
            **access_cookie_directives
        )

        response_object.set_cookie(
            'refresh_token',
            tokens_dict['refresh'],
            **cookie_directives,
            **refresh_cookie_directives
        )

        return response_object

    def generate_expires(self, expire):
        now = datetime.datetime.now()
        expire_date_for_cookie = now + expire
        return expire_date_for_cookie

    def generate_specific_cookie_directives(self, target_string):
        """Genera a dictionary with specific metadata for cookies, this method needs a target with the name in string"""

        max_age_str = 'max_age'
        max_age_target = f"{target_string}_{max_age_str}"

        expires_str = 'expires'
        expires_target = f"{target_string}_{expires_str}"

        cookie_directives = {}

        # Max_age for cookie
        self_max_age = getattr(self, max_age_target)
        if self_max_age is not None:
            cookie_directives['max_age'] = self_max_age
        else:
            cookie_directives['max_age'] = settings.COOKIES_SETTING[max_age_target]

        # Expires for cookie, Django do this by default with max_age directive.
        self_expires = getattr(self, expires_target)
        if self_expires is not None:
            cookie_directives['expires'] = self.generate_expires(self_expires)

        return cookie_directives
