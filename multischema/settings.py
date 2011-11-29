from django.conf import settings


MULTISCHEMA_DEFAULT_NAMESPACE = str(getattr(settings, 'MULTISCHEMA_DEFAULT_NAMESPACE', 'public'))
MULTISCHEMA_APPEND_DEFAULT_NAMESPACE = bool(getattr(settings, 'MULTISCHEMA_APPEND_DEFAULT_NAMESPACE', False))
MUTLISCHEMA_ALIAS_HANDLER = getattr(settings, 'MUTLISCHEMA_ALIAS_HANDLER', 'multischema.handlers.default_alias_handler')
MULTISCHEMA_CREATE_IF_NOT_EXIST = bool(getattr(settings, 'MULTISCHEMA_CREATE_IF_NOT_EXIST', True))

MULTISCHEMA_NAMESPACE_SUPPORTED_BACKENDS = tuple(getattr(settings, 'MULTISCHEMA_NAMESPACE_SUPPORTED_BACKENDS', (
    'django.db.backends.postgresql_psycopg2',
)))
