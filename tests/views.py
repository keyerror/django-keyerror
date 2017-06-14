from django.http import HttpResponse, Http404

from django_keyerror import group_errors


def success(request):
    return HttpResponse('')


def not_found(request):
    raise Http404


def error(request):
    1/0


def error_grouped(request):
    with group_errors('ident'):
        1/0
