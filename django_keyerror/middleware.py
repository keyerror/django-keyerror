import time
import socket

from django.utils import simplejson
from django.core.exceptions import MiddlewareNotUsed

from . import app_settings

class KeyErrorMiddleware(object):
    def __init__(self):
        if not app_settings.ENABLED:
            raise MiddlewareNotUsed()

    def process_view(self, request, callback, callback_args, callback_kwargs):
        view = '%s.' % callback.__module__

        try:
            view += callback.__name__
        except (AttributeError, TypeError):
            # Some view functions (eg. class-based views) do not have a
            # __name__ attribute; try and get the name of its class
            view += callback.__class__.__name__

        request._keyerror_view = view
        request._keyerror_start_time = time.time()

    def process_response(self, request, response):
        try:
            view = request._keyerror_view
            time_taken = time.time() - request._keyerror_start_time
        except AttributeError:
            # If, for whatever reason, the variables are not available, don't
            # do anything else.
            return response

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.sendto(simplejson.dumps({
            'uri': request.path,
            'view': request._keyerror_view,
            'time': time_taken,
            'secret_key': app_settings.SECRET_KEY,
        }), (app_settings.HOST, app_settings.PORT))

        return response
