import mock

from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.management import call_command, CommandError

from django_keyerror import utils
from django_keyerror.api import group_errors
from django_keyerror.app_settings import NOT_PROVIDED

class SmokeTest(TestCase):
    def test_keyerror_deployment_notification(self):
        with self.assertRaises(CommandError):
            call_command(
                'keyerror_deployment_notification',
                "Deployment title",
                "https://example.org/",
            )

    def test_group_errors(self):
        with self.assertRaises(utils.WrappedException) as exc:
            with group_errors('name'):
                1/0

        exc_type, _, _ = exc.exception.exc_info

        self.assertEqual(exc_type, ZeroDivisionError)
        self.assertEqual(exc.exception.ident, 'name')

    def test_smoke_test_django_lightweight_queue(self):
        from django_keyerror import django_lightweight_queue

    def test_smoke_test_middleware(self):
        from django_keyerror import middleware

    @mock.patch('django_keyerror.utils.send_datagram')
    def test_ping(self, mock_send_datagram):
        utils.ping()

        mock_send_datagram.assert_called_once_with(
            'KE\x00\x00\xd4\xba\xccN\xfcZl\n\xc3\x89\xcc\xa5WN\xa7\xec~\x84\x18\xdc',
        )

    @mock.patch('django_keyerror.utils.send_datagram')
    def test_report_response(self, mock_send_datagram):
        utils.report_response("https://example.org/", 'path.to.view', 100)

        mock_send_datagram.assert_called_once_with(
            'KE\x00\x01\xd4\xba\xccN\xfcZl\n\xc3\x89\xcc\xa5WN\xa7'
            '\xec~\x84\x18\xdc\x00\x00\x00d\x00\x14'
            'https://example.org/\x00\x0cpath.to.view'
        )

    def test_success(self):
        self.client.get(reverse('success'))

    def test_not_found(self):
        self.client.get(reverse('not-found'))

    def test_error(self):
        with self.assertRaises(ZeroDivisionError):
            self.client.get(reverse('error'))
