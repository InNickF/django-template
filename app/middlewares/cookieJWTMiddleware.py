"""Cookie JWT Middleware

    This middleware take a new JSON web tokens if these exist after the view and rewrite the cookies with the tokens.
"""

# App imports
from app.utils.authentication import SetJWTCookiesInResponseObject


class CookieJWTMiddleware:
    """Cookie JWT Middleware

    This middleware take a new JSON web tokens if these exist after the view and rewrite the cookies with the tokens.
    """

    def __init__(self, get_response):
        """Middleware initialization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called"""
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        if hasattr(request, 'auth'):
            if isinstance(request.auth, dict):
                if 'new_tokens' in request.auth and request.auth['new_tokens'] is not None:
                    jwtCookiesGenerator = SetJWTCookiesInResponseObject()
                    response = jwtCookiesGenerator.generate(request.auth['new_tokens'], response)

        unauthorized_http_code = 401
        if response.status_code == unauthorized_http_code:
            if 'access_token' in request.COOKIES:
                response.delete_cookie('access_token')
            if 'refresh_token' in request.COOKIES:
                response.delete_cookie('refresh_token')

        return response
