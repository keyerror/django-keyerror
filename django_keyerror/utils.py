import socket
import struct
import binascii

from .app_settings import app_settings

TYPE_PING, TYPE_RESPONSE = range(2)

def ping():
    _send(TYPE_PING)

def report_response(uri, view, elapsed_ms):
    _send(TYPE_RESPONSE, 'I', elapsed_ms, vargs=(uri, view))


def _send(type_, fmt='', *args, **kwargs):
    fmt = '!2sH20s%s' % fmt

    args = [
        'KE',
        type_,
        binascii.unhexlify(app_settings.SECRET_KEY),
    ] + list(args)

    for x in kwargs.pop('vargs', ()):
        x = x.encode('utf-8')
        fmt += 'H%ds' % len(x)
        args.extend((len(x), x))

    datagram = struct.pack(fmt, *args)

    if app_settings.ENABLED: # praga: no-cover
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(
            datagram,
            (app_settings.HOST, app_settings.PORT),
        )

def from_dotted_path(fullpath):
    """
    Returns the specified attribute of a module, specified by a string.

    ``from_dotted_path('a.b.c.d')`` is roughly equivalent to::

        from a.b.c import d

    except that ``d`` is returned and not entered into the current namespace.
    """

    module, attr = fullpath.rsplit('.', 1)

    return getattr(__import__(module, {}, {}, (attr,)), attr)

def get_user_info(request):
    return {}

class WrappedException(Exception):
    def __init__(self, ident, exc_type, exc_value, exc_traceback):
        self.ident = ident

        self.exc_type = exc_value
        self.exc_value = exc_value
        self.exc_traceback = exc_traceback

        super(WrappedException, self).__init__()

def unwrap_exception(exc_type, exc_value, exc_traceback):
    # If we are grouping, extract the unique identifier and override the
    # exception values themselves.
    if isinstance(exc_type, WrappedException):
        exc_type, exc_value, exc_traceback, ident = \
            exc_value.exc_type, exc_value.exc_value, exc_value.exc_traceback, exc_value.ident

    # ..otherwise just return whatever we were passed.
    return exc_type, exc_value, exc_traceback, None
