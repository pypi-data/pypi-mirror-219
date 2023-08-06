from unittest.mock import patch

from django.core.mail.message import EmailMultiAlternatives
from django.test.utils import override_settings
from django.core.mail import send_mail
from django.test import TestCase

from djmailer.backend import EmailBackend
from djmailer.tasks import send_email_by_mailersend


@override_settings(
    DEBUG=True,
    EMAIL_BACKEND='djmailer.backend.EmailBackend',
    DJMAILER_FROM_EMAIL='verified@mail.com',
    DJMAILER_FROM_NAME='Verified Name',
)
class TestMailerEmailBackend(TestCase):
    path_to_celery_task = 'djmailer.tasks.send_email_by_mailersend.delay'
    path_to_pr_send_email = 'djmailer.backend.EmailBackend._send_email'

    @override_settings(DEBUG=True)
    def test_pr_send_email_if_debug_true(self) -> None:
        with patch(self.path_to_celery_task) as send_email_task:
            send_mail(
                'Subject here',
                'Here is the message.',
                'from@example.com',
                ['to1@example.com', 'to2@example.com'],
            )
            send_email_task.assert_not_called()

    @override_settings(DEBUG=False)
    def test_pr_send_email_if_debug_false(self) -> None:
        with patch(self.path_to_celery_task) as send_email_task:
            send_mail(
                'Subject here',
                'Here is the message.',
                'from@example.com',
                ['to1@example.com', 'to2@example.com'],
            )
            send_email_task.assert_called_once()

    def test_message_sent_by_backend(self) -> None:
        with patch('djmailer.backend.EmailBackend.send_messages') as email_send:
            send_mail(
                'Subject here',
                'Here is the message.',
                'from@example.com',
                ['to1@example.com', 'to2@example.com'],
            )
            email_send.assert_called_once()

    def test_email_with_html(self) -> None:
        with patch(self.path_to_pr_send_email) as send_email:
            send_mail(
                'Subject here',
                'Here is the message.',
                'from@example.com',
                ['to1@example.com', 'to2@example.com'],
                html_message='<h1>Hello!</h1>'
            )
            send_email.assert_called_once()
            args, _ = send_email.call_args
            mail_body = args[0]
            self.assertIn('html', mail_body.keys())
            self.assertEqual(mail_body['html'], '<h1>Hello!</h1>')

    def test_bytes_attachments(self) -> None:
        with patch(self.path_to_pr_send_email) as send_email:
            mail = EmailMultiAlternatives(
                'Subject here',
                'Here is the message.',
                to=['to1@example.com', 'to2@example.com'],
            )
            mail.attach('hello.txt', b'Hello world!', 'image/png')
            mail.send()
            args, _ = send_email.call_args
            mail_body = args[0]
            self.assertIn('attachments', mail_body.keys())
            attached_file = mail_body['attachments'][0]
            self.assertIn('content', attached_file.keys())
            self.assertEqual('SGVsbG8gd29ybGQh', attached_file['content'])
            send_email.assert_called_once()

    def test_plain_attachment(self) -> None:
        with patch(self.path_to_pr_send_email) as send_email:
            mail = EmailMultiAlternatives(
                'Subject here',
                'Here is the message.',
                to=['to1@example.com', 'to2@example.com'],
            )
            mail.attach('hello.txt', 'Hello world!', 'text/plain')
            mail.send()
            args, _ = send_email.call_args
            mail_body = args[0]
            self.assertIn('attachments', mail_body.keys())
            attached_file = mail_body['attachments'][0]
            self.assertIn('content', attached_file.keys())
            self.assertEqual('SGVsbG8gd29ybGQh', attached_file['content'])
            send_email.assert_called_once()

    def test_multiple_mailing(self) -> None:
        with patch(self.path_to_pr_send_email) as send_email:
            mail = EmailMultiAlternatives(
                'Subject here',
                'Here is the message.',
                to=[f'to{i}@example.com' for i in range(200)],
            )
            mail.attach('hello.txt', b'Hello world!', 'image/png')
            mail.send()
            self.assertEqual(send_email.call_count, 4)

    def test_empty_to_email_mailing(self) -> None:
        with patch(self.path_to_pr_send_email) as send_email:
            mail = EmailMultiAlternatives(
                'Subject here',
                'Here is the message.',
                to=[],
            )
            mail.attach('hello.txt', b'Hello world!', 'image/png')
            mail.send()
            send_email.assert_not_called()


class TestCeleryTasks(TestCase):
    mail = EmailMultiAlternatives(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@email.com', ],
        )
    mail_body = EmailBackend()._parse_email_message(mail)

    def test_send_email_by_mailersend_202(self) -> None:
        with self.assertLogs('emails', level='DEBUG') as email_logger:
            with patch('mailersend.emails.NewEmail.send') as mock:
                mock.return_value = '202\nAccepted'
                send_email_by_mailersend(self.mail_body)
                mock.assert_called_once_with(self.mail_body)
                self.assertEqual(
                    email_logger.output,
                    [f'INFO:emails:Sent an email to {["to@email.com", ]}']
                )

    def test_send_email_by_mailersend_429(self) -> None:
        with patch('time.sleep') as sleep:
            with self.assertLogs('emails', level='DEBUG') as email_logger:
                with patch('mailersend.emails.NewEmail.send') as mock:
                    mock.side_effect = [
                        '429\nToo Many Requests',
                        '202\nAccepted'
                    ]
                    send_email_by_mailersend(self.mail_body)
                    mock.assert_called_with(self.mail_body)
                    self.assertEqual(mock.call_count, 2)
                    sleep.assert_called_once_with(5)
                    self.assertEqual(
                        email_logger.output, [
                            'DEBUG:emails:Waiting 5 seconds before new try...',
                            f'INFO:emails:Sent an email to {["to@email.com", ]}'
                        ]
                    )

    def test_send_email_by_mailersend_error(self) -> None:
        with self.assertLogs('emails', level='DEBUG') as email_logger:
            with patch('mailersend.emails.NewEmail.send') as mock:
                mock.return_value = '400\nBad Request'
                send_email_by_mailersend(self.mail_body)
                mock.assert_called_with(self.mail_body)
                self.assertEqual(
                    email_logger.output, [
                        f'ERROR:emails:Something went wrong: '
                        f'{["to@email.com", ]}, '
                        'result: Bad Request, code: 400'
                    ]
                )
