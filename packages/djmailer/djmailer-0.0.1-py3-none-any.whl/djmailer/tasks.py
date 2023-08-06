from typing import Dict

import logging
import time

from django.conf import settings
from mailersend import emails
from celery import shared_task


logger = logging.getLogger('emails')


@shared_task(name='djmailer_send_email')
def send_email_by_mailersend(mail_body: Dict) -> None:
    sending = True
    email = [to_mail['email'] for to_mail in mail_body['to']]
    mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)
    while sending:
        code, result = mailer.send(mail_body).split('\n')
        if int(code) == 202:
            logger.info(f'Sent an email to {email}')
            sending = False
        elif int(code) == 429:
            logger.debug('Waiting 5 seconds before new try...')
            time.sleep(5)
        else:
            logger.error(
                f'Something went wrong: {email}, '
                f'result: {result}, code: {code}'
            )
            sending = False
