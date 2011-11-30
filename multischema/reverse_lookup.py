from django.core.urlresolvers import get_callable

from multischema import settings


def mapping(alias, default=settings.MULTISCHEMA_REVERSE_LOOKUP_DEFAULT):
    lookup = None
    
    if alias in settings.MULTISCHEMA_REVERSE_LOOKUP_MAPPING:
        lookup = settings.MULTISCHEMA_REVERSE_LOOKUP_MAPPING[alias]
    elif default:
        lookup = default
    else:
        default_handler = get_callable(settings.MULTISCHEMA_REVERSE_LOOKUP_DEFAULT_HANDLER)
        lookup = default_handler(alias)
    return lookup
