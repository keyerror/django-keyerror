import sys
import logging

from django.http import Http404
from django.conf import settings
from django.core.signals import got_request_exception

from .utils import unwrap_exception
from .error import DjangoError, QueueError
from .app_settings import app_settings

logger = logging.getLogger(__name__)

## Django ####################################################################

def report_exception(sender, request, **kwargs):
    if not app_settings.ENABLED:
        return

    exc_type, exc_value, exc_traceback, ident = \
        unwrap_exception(*sys.exc_info())

    # Ignore some errors
    if isinstance(exc_type, (Http404, SystemExit)):
        return

    try:
        DjangoError(request, exc_type, exc_value, exc_traceback, ident).send()
    except Exception:
        logger.exception("Exception whilst reporting error to keyerror.com")

got_request_exception.connect(report_exception)

## Celery ####################################################################

if 'djcelery' in settings.INSTALLED_APPS:
    from celery import signals

    def report_task_failure(einfo, traceback, **kwargs):
        if not app_settings.ENABLED:
            return

        exc_type, exc_value, exc_traceback, ident = \
            unwrap_exception(einfo.type, einfo.exception, traceback)

        try:
            QueueError(exc_type, exc_value, exc_traceback, ident).send()
        except Exception:
            logger.exception("Exception whilst reporting error to keyerror.com")

    signals.task_failure.connect(report_task_failure)
