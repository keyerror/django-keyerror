import socket
import struct
import binascii

from . import app_settings

TYPE_PING, TYPE_RESPONSE = range(2)

def ping():
    _send(TYPE_PING)

def report_response(uri, view, time_taken):
    _send(TYPE_RESPONSE, 'I', time_taken, vargs=(uri, view))


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

    socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(
        struct.pack(fmt, *args),
        (app_settings.HOST, app_settings.PORT),
    )
