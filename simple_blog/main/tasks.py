import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from application.celery import app


@app.task
def send_verification_email(user_id):

    user_model = get_user_model()
    try:
        user = user_model.objects.get(pk=user_id)
        send_mail(
            'Verify your Publisher account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )
    except user_model.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
