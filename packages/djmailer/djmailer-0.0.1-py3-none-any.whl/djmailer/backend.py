from typing import Dict, List, Union

from base64 import b64encode
import logging

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

from djmailer.tasks import send_email_by_mailersend


logger = logging.getLogger('emails')


class EmailBackend(BaseEmailBackend):
    @staticmethod
    def _send_email(mail_body: Dict) -> None:
        to_emails = [to_mail['email'] for to_mail in mail_body['to']]
        mail_subject = mail_body['subject']
        if not settings.DEBUG:
            logger.info(f"Sending email to {to_emails}"
                        f" with subject {mail_subject}...")
            send_email_by_mailersend.delay(mail_body)
            logger.info(f"Task has been assigned to"
                        f"celery: email to {to_emails}")
        else:
            logger.debug(f"Sending email to {to_emails}"
                         f" with subject {mail_subject}")

    @staticmethod
    def _convert_email_address_for_mailersend(
                email: Union[str, List[str]]
            ) -> List[Dict[str, str]]:
        return [{'email': email_address, } for email_address in email]

    def _parse_email_message(
                self, django_email: EmailMultiAlternatives
            ) -> Dict:
        mail_body = {
            'text': django_email.body,
            'subject': django_email.subject,
            'from': {
                    'email': settings.DJMAILER_FROM_EMAIL,
                    'name': settings.DJMAILER_FROM_NAME,
                },
            'to': self._convert_email_address_for_mailersend(
                    django_email.to
                ),
            'reply_to': self._convert_email_address_for_mailersend(
                    django_email.reply_to
                ),
            'cc': self._convert_email_address_for_mailersend(
                    django_email.cc
                ),
            'bcc': self._convert_email_address_for_mailersend(
                    django_email.bcc
                ),
        }

        for content, mimetype in django_email.alternatives:
            if mimetype == 'text/html':
                mail_body['html'] = content
        if django_email.attachments:
            mail_body['attachments'] = list()
            for filename, content, _ in django_email.attachments:
                if isinstance(content, str):
                    content = content.encode('utf-8')
                mail_body['attachments'].append({
                    'filename': filename,
                    'content': b64encode(content).decode('utf-8'),
                    'disposition': 'attachment'
                })
        return mail_body

    def _send(self, email_message: EmailMultiAlternatives) -> None:
        recipients = email_message.recipients()
        # if there are more than 50 recipients
        # we need to divide them by 50
        # since mailersend has a limit
        if len(recipients) > 50:
            chunked_emails = [recipients[i:i + 50]
                              for i in range(0, len(recipients), 50)]
            for email in chunked_emails:
                email_message.to = email
                mail_body = self._parse_email_message(email_message)
                self._send_email(mail_body)
        else:
            mail_body = self._parse_email_message(email_message)
            self._send_email(mail_body)

    def send_messages(
                self, email_message: List[EmailMultiAlternatives]
            ) -> None:
        if len(email_message) == 0:
            return  # pragma: no cover
        for message in email_message:
            self._send(message)
