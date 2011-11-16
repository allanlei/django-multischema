from django.db.backends.signals import connection_created
from django.utils.importlib import import_module

import settings
from signals import create_namespace_if_not_exist, switch_to_namespace_on_connect


if settings.MULTISCHEMA_CREATE_IF_NOT_EXIST:
    for backend in settings.MULTISCHEMA_NAMESPACE_SUPPORTED_BACKENDS:
        connection_created.connect(create_namespace_if_not_exist, sender=import_module(backend).base.DatabaseWrapper)

for backend in settings.MULTISCHEMA_NAMESPACE_SUPPORTED_BACKENDS:
    connection_created.connect(switch_to_namespace_on_connect, sender=import_module(backend).base.DatabaseWrapper)
