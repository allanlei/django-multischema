from django.conf import settings


MULTISCHEMA_DEFAULT_SCHEMA = str(getattr(settings, 'MULTISCHEMA_DEFAULT_SCHEMA', 'public'))
MULTISCHEMA_APPEND_DEFAULT_PATH = bool(getattr(settings, 'MULTISCHEMA_APPEND_DEFAULT_PATH', False))
MULTISCHEMA_CONNECT_SET_PATH_HANDLER = getattr(settings, 'MULTISCHEMA_CONNECT_SET_PATH_HANDLER', 'multischema.utils.default_set_path')
MULTISCHEMA_CREATE_IF_NOT_EXIST = bool(getattr(settings, 'MULTISCHEMA_CREATE_IF_NOT_EXIST', True))
MULTISCHEMA_EXCLUDE_ALIASES = tuple(getattr(settings, 'MULTISCHEMA_EXCLUDE_ALIASES', (
    'default',
)))

MULTISCHEMA_NAMESPACE_SUPPORTED_BACKENDS = tuple(getattr(settings, 'MULTISCHEMA_NAMESPACE_SUPPORTED_BACKENDS', (
    'django.db.backends.postgresql_psycopg2',
)))
MULTISCHEMA_ALIAS_MAP = dict(getattr(settings, 'MULTISCHEMA_ALIAS_MAP', {
    'default': 'public',
}))
MULTISCHEMA_DEFAULT_PATH = MULTISCHEMA_DEFAULT_SCHEMA
