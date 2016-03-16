import sys
import logging

from django.http import Http404
from django.conf import settings
from django.core.signals import got_request_exception

from . import app_settings
from .error import DjangoError, QueueError

logger = logging.getLogger(__name__)

## Django ####################################################################

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

## Celery ####################################################################

if 'djcelery' in settings.INSTALLED_APPS:
    from celery import signals

    def report_task_failure(einfo, traceback, **kwargs):
        if not app_settings.ENABLED:
            return

        try:
            QueueError(einfo.type, einfo.exception, traceback).send()
        except Exception:
            logger.exception("Exception whilst reporting error to keyerror.com")

    signals.task_failure.connect(report_task_failure)
