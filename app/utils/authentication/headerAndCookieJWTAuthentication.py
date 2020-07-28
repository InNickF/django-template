"""Header and Cookie JWT Authentication

    This class is inheriting from JWTAuthentication (Simple JWT) and is used for authenticate user with JWT via HTTP headers and Cookies HttpOnly
"""

# Django imports
from django.utils.translation import gettext_lazy as _

# Django Rest Framework Simple JWT imports
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class HeaderAndCookieJWTAuthentication(JWTAuthentication):
    """
    This authenticate method search in header and cookies for a JWT if
    the method used for the front-end for authentication is cookie
    also refresh the JWT if is necessary.

    This method is used in settings file > REST_FRAMEWORK > DEFAULT_AUTHENTICATION_CLASSES
    """

    def authenticate(self, request):
        is_header_method = self.auth_with_header(request)

        if is_header_method is None:
            is_cookie_method = self.auth_with_cookie(request)

            if is_cookie_method is None:
                return None

            return is_cookie_method['user'], {
                'validated_token': is_cookie_method['validated_token'],
                'new_tokens': is_cookie_method['new_tokens']
            }

        else:
            return is_header_method['user'], {
                'validated_token': is_header_method['validated_token'],
                'new_tokens': None
            }

    def auth_with_header(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return {
            'user': self.get_user(validated_token),
            'validated_token': validated_token
        }

    def auth_with_cookie(self, request):
        if 'access_token' in request.COOKIES and 'refresh_token' in request.COOKIES:
            raw_token = request.COOKIES['access_token']
            refresh_token = request.COOKIES['refresh_token']
            validated_token, new_tokens = self.get_validated_token(raw_token, refresh_token)

            return {
                'user': self.get_user(validated_token),
                'validated_token': validated_token,
                'new_tokens': new_tokens,
            }

        return None

    def get_validated_token(self, raw_token, refresh_token=None):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                if refresh_token is None:
                    return AuthToken(raw_token)
                else:
                    return AuthToken(raw_token), None
            except TokenError as e:
                if refresh_token is None:
                    messages.append({'token_class': AuthToken.__name__,
                                     'token_type': AuthToken.token_type,
                                     'message': e.args[0]})
                else:
                    try:
                        refresh = RefreshToken(refresh_token)
                        new_tokens = {'access': str(refresh.access_token)}
                        if api_settings.ROTATE_REFRESH_TOKENS:
                            if api_settings.BLACKLIST_AFTER_ROTATION:
                                try:
                                    # Attempt to blacklist the given refresh token
                                    refresh.blacklist()
                                except AttributeError as e:
                                    messages.append({
                                        'Error:': e.args[0]
                                    })

                            refresh.set_jti()
                            refresh.set_exp()
                            new_tokens['refresh'] = str(refresh)
                        return AuthToken(new_tokens['access']), new_tokens

                    except Exception as e:
                        messages.append({
                            'Error:': e.args[0]
                        })

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })
