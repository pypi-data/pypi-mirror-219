from django_glue.conf import settings
from django_glue import __version__


def glue(request):
    return {
        'DJANGO_GLUE_VERSION': __version__,
        settings.DJANGO_GLUE_CONTEXT_NAME: request.session.get(settings.DJANGO_GLUE_SESSION_NAME, {}).get('context'),
        settings.DJANGO_GLUE_KEEP_LIVE_CONTEXT_NAME: request.session.get(settings.DJANGO_GLUE_KEEP_LIVE_SESSION_NAME, {}),
        'DJANGO_GLUE_KEEP_LIVE_INTERVAL_TIME_MILLISECONDS': settings.DJANGO_GLUE_KEEP_LIVE_INTERVAL_TIME_SECONDS * 1000,
    }
