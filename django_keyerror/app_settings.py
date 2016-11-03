from django.core import mail
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

TEMPLATE = 'KEYERROR_%s'

class NOT_PROVIDED:
    pass

def setting(suffix, default=NOT_PROVIDED):
    # Lazily get settings from ``django.conf.settings`` instance so that the
    # @override_settings works.
    @property
    def fn(self):
        key = TEMPLATE % suffix

        try:
            if default is NOT_PROVIDED:
                return getattr(settings, key)
        except AttributeError:
            raise ImproperlyConfigured(
                "Missing required setting: {}".format(key)
            )

        return getattr(settings, key, default)

    return fn

class AppSettings(object):
    SECRET_KEY = setting('SECRET_KEY')

    USER_INFO_CALLBACK = setting(
        'USER_INFO_CALLBACK',
        'django_keyerror.utils.get_user_info',
    )

    URL = setting('URL', 'http://api.keyerror.com/v1%s')
    TIMEOUT = setting('TIMEOUT', 1)

    HOST = setting('HOST', 'api.keyerror.com')
    PORT = setting('PORT', 2930)

    @property
    def ENABLED(self):
        # Always respect ENABLED if specified
        try:
            return getattr(settings, TEMPLATE % 'ENABLED')
        except AttributeError:
            # If we haven't overridden this, first check we aren't running tests
            if self.IS_TEST:
                return False

            # .. then assume that if we are debugging, we don't want to run i
            return not settings.DEBUG

    @property
    def IS_TEST(self):
        return hasattr(mail, 'outbox')

app_settings = AppSettings()
