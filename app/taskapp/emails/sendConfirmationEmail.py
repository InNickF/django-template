"""Confirmation email to user"""

# Django imports
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.conf import settings

# Celery imports
from celery import current_app

# App imports
from app.utils.jwt.manuallyTokens import VerificationUserToken
from app.users.models import User


class SendConfirmationEmail(current_app.Task):
    name = 'tasks.send_confirmation_email'

    def run(self, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
            self.send_email_to(user)
        except Exception as e:
            raise str(e.args[0])

    def get_token_for_email(self, user):
        jwt = VerificationUserToken()
        token = jwt.generate(user)
        return token

    def send_email_to(self, user):
        token = self.get_token_for_email(user)
        context = {
            'user': user,
            'token': token,
        }
        subject = f"Welcome, {user.username}! It's time to verify your account"
        text_content = render_to_string('emails/account_verification.html', context)
        html_content = get_template('emails/account_verification.html').render(context)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email
        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [to]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


current_app.tasks.register(SendConfirmationEmail())
