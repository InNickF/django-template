"""Verification user token

    This token is use for verification emails
"""

# Django imports
from django.utils import timezone
from django.conf import settings

# PyJWT
import jwt

# Utils
from datetime import timedelta


class VerificationUserToken():

    def __init__(self):
        self.key = settings.SECRET_KEY

    def generate(self, user):
        max_days = 1
        exp_date = timezone.now() + timedelta(days=max_days)
        payload = {
            'user': user.id,
            'exp': int(exp_date.timestamp()),
            'token_type': 'email_confirmation'
        }

        token = jwt.encode(payload, self.key, algorithm='HS256')

        return token.decode()

    def decode(self, tokenStr):
        """Verify JWT"""
        try:
            payload = jwt.decode(tokenStr, self.key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError('Verification token has expired.')
        except jwt.PyJWTError:
            raise jwt.PyJWTError('Invalid token')
        if payload['token_type'] != 'email_confirmation':
            raise jwt.PyJWTError('Invalid token')

        return payload
