import time
import logging

from .utils import report_response
from .app_settings import app_settings

logger = logging.getLogger(__name__)


class KeyErrorMiddleware(object):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if not app_settings.ENABLED:
            return

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
        if not app_settings.ENABLED:
            return response

        try:
            elapsed_ms = int((time.time() - request._keyerror_start_time) * 1000)
            view_name = request._keyerror_view
        except AttributeError:  # pragma: no cover
            # If, for whatever reason, the variables are not available, don't
            # do anything else.
            return response

        try:
            report_response(request.path, view_name, elapsed_ms)
        except:  # pragma: no cover
            # Log the exception but don't interrupt the request
            logger.exception("Exception whilst reporting error to keyerror.com")

        return response
