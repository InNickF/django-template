"""All tasks"""

# Django imports
from django.utils import timezone

# Celery imports
# from celery.task.schedules import crontab
from celery.decorators import periodic_task

# Emails
from .emails import SendConfirmationEmail

# Utils
from datetime import timedelta


# @periodic_task(name='disable_finished_rides', run_every=timedelta(minutes=60))
# def disable_finished_rides():
#     """Disable finished rides."""
#     now = timezone.now()
#     offset = now + timedelta(minutes=60)

#     # Update rides that have already finished
#     rides = Ride.objects.filter(
#         arrival_date__gte=now,
#         arrival_date__lte=offset,
#         is_active=True
#     )
#     rides.update(is_active=False)
