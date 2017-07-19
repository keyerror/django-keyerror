from six.moves import urllib

from django.core.management.base import BaseCommand, CommandError

from ...app_settings import app_settings


class Command(BaseCommand):
    help = "Notify KeyError of a new deployment."
    args = '[options] "<deployment title>" "<deployment url>"'
    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument('title')
        parser.add_argument('url')

    def handle(self, *args, **options):
        post_url = app_settings.URL % '/deployments'

        req = urllib.request.Request(post_url, urllib.parse.urlencode({
            'url': options['url'],
            'title': options['title'],
        }).encode('ascii'), {
            'X-API-Key': app_settings.SECRET_KEY,
        })

        if not app_settings.ENABLED:
            raise CommandError("KeyError is not enabled; exiting.")

        try: # pragma: no cover
            urllib.request.urlopen(req, timeout=5)
        except urllib.error.HTTPError as exc: # pragma: no cover
            raise CommandError("Error when notifying KeyError: %s" % exc)
