from django.core.exceptions import MiddlewareNotUsed

from .error import QueueError
from .app_settings import app_settings

class KeyErrorMiddleware(object):
    def __init__(self):
        if not app_settings.ENABLED:
            raise MiddlewareNotUsed()

    def process_exception(self, job, duration, *exc_info):
        QueueError(*exc_info).send()
