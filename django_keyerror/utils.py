import json
import socket

from . import app_settings

def report_response(uri, view, time_taken):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(json.dumps({
        'uri': uri,
        'view': view,
        'time': time_taken,
        'secret_key': app_settings.SECRET_KEY,
    }), (app_settings.HOST, app_settings.PORT))
