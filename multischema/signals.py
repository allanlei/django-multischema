from django.dispatch import Signal

import logging
logger = logging.getLogger(__name__)


pre_switch = Signal(providing_args=[])
post_switch = Signal(providing_args=[])

pre_create = Signal(providing_args=[])
post_create = Signal(providing_args=[])

pre_rename = Signal(providing_args=[])
post_rename = Signal(providing_args=[])

pre_drop = Signal(providing_args=[])
post_drop = Signal(providing_args=[])



from django.core.urlresolvers import get_callable

import settings
import utils
import helpers

set_path_handler = get_callable(settings.MULTISCHEMA_CONNECT_SET_PATH_HANDLER)


def create_namespace_if_not_exist(sender, connection, **kwargs):
    connected_alias = helpers.get_connection_alias(connection)
        
    if connected_alias and connected_alias not in settings.MULTISCHEMA_EXCLUDE_ALIASES:
        cursor = connection.cursor()
        utils.create_namespace(connected_alias, cursor=cursor)

def switch_to_namespace_on_connect(sender, connection, **kwargs):
    connected_alias = helpers.get_connection_alias(connection)
        
    if connected_alias:
        namespaces = set_path_handler(alias=connected_alias)
        if namespaces:
            cursor = connection.cursor()
            utils.switch_namespace(*namespaces, cursor=cursor)
