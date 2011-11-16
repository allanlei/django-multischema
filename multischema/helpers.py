from django.db import connections

import settings

def get_connection_alias(connection):
    connected_alias = None
    for alias, conn in connections._connections.items():
        if conn == connection:
            connected_alias = alias
            break
    return connected_alias
    
def default_set_path(alias=None):
    paths = []
    if alias:
        paths.append(settings.MULTISCHEMA_ALIAS_MAP.get(alias, alias))
        
    if settings.MULTISCHEMA_APPEND_DEFAULT_PATH:
        paths.append(settings.MULTISCHEMA_DEFAULT_SCHEMA)
    return paths
