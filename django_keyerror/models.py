import sys
import logging

from django.http import Http404
from django.core.signals import got_request_exception

from . import app_settings
from .error import DjangoError

logger = logging.getLogger(__name__)

def report_exception(sender, request, **kwargs):
    if not app_settings.ENABLED:
        return

    exc_type, exc_value, exc_traceback = sys.exc_info()

    if isinstance(exc_type, (Http404, SystemExit)):
        return

    try:
        DjangoError(request, exc_type, exc_value, exc_traceback).send()
    except Exception:
        logger.exception("Exception whilst reporting error to keyerror.com")

got_request_exception.connect(report_exception)
