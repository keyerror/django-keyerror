import time
import logging

from django.core.exceptions import MiddlewareNotUsed

from . import app_settings
from .utils import report_response

logger = logging.getLogger(__name__)

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
            elapsed = int((time.time() - request._keyerror_start_time) * 1000)
            view_name = request._keyerror_view
        except AttributeError:
            # If, for whatever reason, the variables are not available, don't
            # do anything else.
            return response

        try:
            report_response(request.path, view_name, elapsed)
        except:
            # Log the exception but don't interrupt the request
            logger.exception("Exception whilst reporting error to keyerror.com")

        return response
