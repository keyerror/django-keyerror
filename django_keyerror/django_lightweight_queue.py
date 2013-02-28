from django.core.exceptions import MiddlewareNotUsed

from . import app_settings
from .error import QueueError

class KeyErrorMiddleware(object):
    def __init__(self):
        if not app_settings.ENABLED:
            raise MiddlewareNotUsed()

    def process_exception(self, job, duration, *exc_info):
        QueueError(*exc_info).send()
