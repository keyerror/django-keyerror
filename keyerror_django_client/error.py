import sys
import urllib
import socket
import logging
import urllib2
import traceback

from django.conf import settings
from django.utils import simplejson

from . import app_settings

logger = logging.getLogger(__name__)

class Error(dict):
    def __init__(self, request, exc_type, exc_value, exc_traceback):
        tb = traceback.extract_tb(exc_traceback)
        synopsis = traceback.format_exception_only(exc_type, exc_value)[-1]

        self.update({
            'url': request.build_absolute_uri()[:200],
            'server': socket.gethostname()[:100],
            'synopsis': synopsis.strip()[:200],
            'traceback': simplejson.dumps(tb),

            'apps': simplejson.dumps(settings.INSTALLED_APPS),
            'exc_type': exc_type.__name__,
            'sys_path': simplejson.dumps(sys.path),
        })

    def send(self):
        logger.debug("Posting error to %s", app_settings.URL)

        req = urllib2.Request(app_settings.URL, urllib.urlencode(self), {
            'X-API-Key': app_settings.SECRET_KEY,
        })

        try:
            kwargs = {}
            # 'timeout' argument only supported in Python 2.6
            if sys.version_info >= (2, 6):
                kwargs['timeout'] = app_settings.TIMEOUT

            urllib2.urlopen(req, **kwargs)
        except urllib2.HTTPError, e:
            try:
                # We try and print a descriptive message on the first line of
                # the response
                e.msg = '%s - %s' % (e.msg, e.read().splitlines()[0])
            except IndexError:
                pass

            raise
