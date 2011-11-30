from django.db.backends.signals import connection_created
from django.utils.importlib import import_module

from multischema import settings
from multischema.handlers import create_namespace_if_not_exist, switch_to_namespace_on_connect


backends = [getattr(import_module('.base', package=backend), 'DatabaseWrapper') for backend in settings.MULTISCHEMA_SUPPORTED_BACKENDS]

if settings.MULTISCHEMA_CREATE_IF_NOT_EXIST:
    for backend in backends:
        connection_created.connect(create_namespace_if_not_exist, sender=backend)

for backend in backends:
    connection_created.connect(switch_to_namespace_on_connect, sender=backend)
