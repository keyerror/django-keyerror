# -*- coding: utf-8 -*-

import sys
import mock

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command, CommandError

from django_keyerror import utils
from django_keyerror.error import Error
from django_keyerror.api import group_errors
from django_keyerror.app_settings import app_settings


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
        django_lightweight_queue

    def test_smoke_test_middleware(self):
        from django_keyerror import middleware
        middleware

    @override_settings()
    def test_missing_settings(self):
        del settings.KEYERROR_SECRET_KEY

        with self.assertRaises(ImproperlyConfigured):
            app_settings.SECRET_KEY

    @override_settings()
    def test_fallback_enabled(self):
        del settings.KEYERROR_ENABLED

        self.failIf(app_settings.ENABLED)

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

    def test_smoke(self):
        with self.assertRaises(ZeroDivisionError):
            self.client.get(reverse('error'))

    @override_settings(KEYERROR_ENABLED=False)
    def test_smoke_disabled(self):
        with self.assertRaises(ZeroDivisionError):
            self.client.get(reverse('error'))

    @mock.patch('django_keyerror.error.Error._send')
    def test_error(self, mock_send):
        with self.assertRaises(ZeroDivisionError):
            self.client.get(reverse('error'))

        self.assertEqual(mock_send.call_count, 1)

        url, data, headers = mock_send.call_args[0]

        self.assertEqual(url, 'http://api.keyerror.com/v1/errors')

        self.assertEqual(
            data['synopsis'],
            "ZeroDivisionError: integer division or modulo by zero",
        )
        self.assertEqual(data['url'], 'http://testserver/error')
        self.assertEqual(data['user'], '{}')
        self.assertEqual(data['type'], 'django')
        self.assertEqual(data['ident'], '')
        self.assertEqual(data['exc_type'], 'ZeroDivisionError')

        self.assert_('apps' in data)
        self.assert_('sys_path' in data)
        self.assert_('traceback' in data)

        self.assertEqual(
            headers['X-API-Key'],
            'd4bacc4efc5a6c0ac389cca5574ea7ec7e8418dc',
        )

    @mock.patch('django_keyerror.error.Error._send')
    def test_error_grouped(self, mock_send):
        try:
            self.client.get(reverse('error-grouped'))
        except Exception:
            pass

        self.assertEqual(mock_send.call_count, 1)
        _, data, _ = mock_send.call_args[0]

        self.assertEqual(data['ident'], 'ident')
        self.assertEqual(data['exc_type'], 'ZeroDivisionError')

    @override_settings(KEYERROR_USER_INFO_CALLBACK='tests.user_info_callback')
    def test_user_info(self):
        with self.assertRaises(ZeroDivisionError):
            self.client.get(reverse('error'))

    def test_unicode_ident(self):
        try:
            1/0
        except:
            Error(*sys.exc_info(), ident=u'unicode-error-é').send()

    def test_unicode_data(self):
        try:
            1/0
        except:
            error = Error(*sys.exc_info(), ident=None)
            error['url'] = u'http://somewhere/unicode-error-é'
            error.send()
