from django.template.loader import render_to_string
from django.core.signing import Signer
from datetime import datetime
from os.path import splitext
from config.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_notification(user):
    """ Send activation notification to user email
    """
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def get_timestamp_path(instance, filename):
    """ Generates the names of uploaded files
    """
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
