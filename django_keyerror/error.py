import sys
import json
import urllib
import socket
import logging
import urllib2
import traceback

from django.conf import settings

from . import app_settings
from .utils import from_dotted_path

logger = logging.getLogger(__name__)

fn_user_info_callback = from_dotted_path(app_settings.USER_INFO_CALLBACK)

class Error(dict):
    def __init__(self, exc_type, exc_value, exc_traceback):
        tb = traceback.extract_tb(exc_traceback)
        synopsis = traceback.format_exception_only(exc_type, exc_value)[-1]

        self.update({
            'server': socket.gethostname()[:100],
            'synopsis': synopsis.strip()[:200],
            'traceback': json.dumps(tb),

            'apps': json.dumps(settings.INSTALLED_APPS),
            'exc_type': exc_type.__name__,
            'sys_path': json.dumps(sys.path),
        })

    def send(self):
        url = app_settings.URL % '/errors'

        logger.debug("Posting error to %s", url)

        req = urllib2.Request(url, urllib.urlencode(self), {
            'X-API-Key': app_settings.SECRET_KEY,
        })

        try:
            kwargs = {}
            # 'timeout' argument only supported in Python 2.6
            if sys.version_info >= (2, 6):
                kwargs['timeout'] = app_settings.TIMEOUT

            urllib2.urlopen(req, **kwargs)
        except urllib2.HTTPError as e:
            try:
                # We try and print a descriptive message on the first line of
                # the response
                e.msg = '%s - %s' % (e.msg, e.read().splitlines()[0])
            except IndexError:
                logger.exception("Exception whilst reporting error to keyerror.com")

            raise

class DjangoError(Error):
    def __init__(self, request, *args, **kwargs):
        super(DjangoError, self).__init__(*args, **kwargs)

        self.update({
            'url': request.build_absolute_uri(),
            'type': 'django',
        })

        try:
            self['user'] = json.dumps(self.get_user_info(request))
        except Exception:
            logger.exception("Exception whilst reporting error to keyerror.com")

    def get_user_info(self, request):
        # Don't depend on contrib.auth
        if hasattr(request, 'user') and request.user.is_authenticated():
            # Try and determine a reasonable default display name. We try not
            # rely on username existing - this field is often removed.
            display = request.user.get_full_name().strip() or \
                getattr(request.user, 'username', '')

            # Set defaults
            user = {
                'url': '',
                'display': display,
                'avatar_url': '',
                'identifier': str(request.user.id),
                'is_authenticated': True,
            }

            # Allow app to override
            user.update(fn_user_info_callback(request))

            return user

        if hasattr(request, 'session') and request.session.session_key:
            return {
                'identifier': request.session.session_key,
                'is_authenticated': False,
            }

        return {}

class QueueError(Error):
    def __init__(self, *args, **kwargs):
        super(QueueError, self).__init__(*args, **kwargs)

        self.update({
            'type': 'queue',
        })
