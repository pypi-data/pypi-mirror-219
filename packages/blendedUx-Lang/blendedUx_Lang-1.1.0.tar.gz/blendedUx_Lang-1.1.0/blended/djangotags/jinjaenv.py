from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from blended.jinjaenv import BlendedEnvironment


def environment(**options):
    env = BlendedEnvironment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
