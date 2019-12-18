import logging

from django.core.mail import send_mail as django_send_mail

logger = logging.getLogger(__name__)


def send_mail(subject, message, from_email,
              recipient_list, fail_silently=False,
              auth_user=None, auth_password=None,
              connection=None, html_message=None):
    """
    Define method for sending email notification.
    """
    try:
        django_send_mail(
            subject, message, from_email, recipient_list,
            fail_silently=fail_silently, auth_user=auth_user,
            auth_password=auth_password, connection=connection,
            html_message=html_message
        )
    except Exception as error:
        logger.error(error)
