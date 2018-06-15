import sys
import json
import mock

from django.test import TestCase
from django_keyerror.error import Error


class Python3Test(TestCase):
    @mock.patch('django_keyerror.error.Error._send')
    def test_traceback_with_context(self, mock_send):
        def inner():
            raise ValueError('inner')

        def outer():
            try:
                inner()
            except ValueError as e:
                raise TypeError('outer')

        try:
            outer()
        except Exception:
            Error(*sys.exc_info()).send()

        self.assertEqual(mock_send.call_count, 1)
        _, data, _ = mock_send.call_args[0]
        traceback = json.loads(data['traceback'])

        self.assertNotIn(
            [mock.ANY, mock.ANY, 'inner', mock.ANY],
            traceback,
            "Traceback should not contain inner function",
        )

        self.assertIn(
            [mock.ANY, mock.ANY, 'outer', mock.ANY],
            traceback,
            "Traceback should contain outer function",
        )

    @mock.patch('django_keyerror.error.Error._send')
    def test_traceback_with_cause(self, mock_send):
        def inner():
            raise ValueError('inner')

        def outer():
            try:
                inner()
            except ValueError as e:
                raise TypeError('outer') from e

        try:
            outer()
        except Exception:
            Error(*sys.exc_info()).send()

        self.assertEqual(mock_send.call_count, 1)
        _, data, _ = mock_send.call_args[0]
        traceback = json.loads(data['traceback'])

        self.assertIn(
            [mock.ANY, mock.ANY, 'inner', mock.ANY],
            traceback,
            "Traceback should contain inner function",
        )

        self.assertIn(
            [mock.ANY, mock.ANY, 'outer', mock.ANY],
            traceback,
            "Traceback should contain outer function",
        )

    @mock.patch('django_keyerror.error.Error._send')
    def test_traceback_with_explicit_none_cause(self, mock_send):
        def inner():
            raise ValueError('inner')

        def outer():
            try:
                inner()
            except ValueError as e:
                raise TypeError('outer') from None

        try:
            outer()
        except Exception:
            Error(*sys.exc_info()).send()

        self.assertEqual(mock_send.call_count, 1)
        _, data, _ = mock_send.call_args[0]
        traceback = json.loads(data['traceback'])

        self.assertNotIn(
            [mock.ANY, mock.ANY, 'inner', mock.ANY],
            traceback,
            "Traceback should not contain inner function",
        )

        self.assertIn(
            [mock.ANY, mock.ANY, 'outer', mock.ANY],
            traceback,
            "Traceback should contain outer function",
        )
