from django.core import mail
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class NOT_PROVIDED:
    pass

def setting(suffix, default=NOT_PROVIDED):
    # Lazily get settings from ``django.conf.settings`` instance so that the
    # @override_settings works.
    @property
    def fn(self):
        key = 'KEYERROR_%s' % suffix

        try:
            if default is NOT_PROVIDED:
                return getattr(settings, key)
        except AttributeError:
            raise ImproperlyConfigured(
                "Missing required setting: {}".format(key),
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
    HOST = setting('HOST', 'api.keyerror.com')
    PORT = setting('PORT', 2930)
    TIMEOUT = setting('TIMEOUT', 1)

    @property
    def ENABLED(self):
        if hasattr(mail, 'outbox'):
            False

        try:
            return setting('ENABLED')
        except ImproperlyConfigured:
            # If we haven't overridden this, fallback to settings.DEBUG
            return not settings.DEBUG

app_settings = AppSettings()
