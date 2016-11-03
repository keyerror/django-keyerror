from django.http import HttpResponse, Http404

def success(request):
    return HttpResponse('')

def not_found(request):
    raise Http404

def error(request):
    1/0
