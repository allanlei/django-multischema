from django.db import connections

import logging
logger = logging.getLogger(__name__)


def get_connection_alias(connection):
    connected_alias = None
    for alias, conn in connections._connections.items():
        if conn == connection:
            connected_alias = alias
            break
    return connected_alias
