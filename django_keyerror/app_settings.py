from django.core import mail
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

PREFIX = 'KEYERROR'

def get_setting(suffix, *args):
    return getattr(settings, '%s_%s' % (PREFIX, suffix), *args)

URL = get_setting('URL', 'http://api.keyerror.com/v1%s')
TIMEOUT = get_setting('TIMEOUT', 1)

USER_INFO_CALLBACK = get_setting(
    'USER_INFO_CALLBACK',
    'django_keyerror.utils.get_user_info',
)

HOST = get_setting('HOST', 'api.keyerror.com')
PORT = get_setting('PORT', 2930)

try:
    ENABLED = get_setting('ENABLED')
except AttributeError:
    # If we haven't overridden this, fallback to settings.DEBUG
    ENABLED = not settings.DEBUG

# Always disble KeyError in a test environment
if hasattr(mail, 'outbox'):
    ENABLED = False

try:
    SECRET_KEY = get_setting('SECRET_KEY')
except AttributeError:
    raise ImproperlyConfigured(
        "Missing required setting: %s_SECRET_KEY" % PREFIX
    )
