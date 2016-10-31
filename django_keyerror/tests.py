from django.test import TestCase, override_settings
from django.core.management import call_command, CommandError

from . import utils

from .api import group_errors
from .app_settings import NOT_PROVIDED

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

        exc_type, exc_value, exc_traceback, ident = utils.unwrap_exception(
            exc.exception.exc_type,
            exc.exception.exc_value,
            exc.exception.exc_traceback,
        )

        self.assert_(isinstance(exc_type, ZeroDivisionError))
        self.assertEqual(ident, 'name')

    def test_smoke_test_django_lightweight_queue(self):
        from . import django_lightweight_queue

    def test_smoke_test_middleware(self):
        from . import middleware

    def test_ping(self):
        utils.ping()

    def test_report_response(self):
        utils.report_response("https://example.org/", 'path.to.view', 100)
