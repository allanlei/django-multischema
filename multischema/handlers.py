from django.core.urlresolvers import get_callable

from multischema import settings
from multischema import namespace
from multischema.utils import get_connection_alias

import logging
logger = logging.getLogger(__name__)



default_mapping = {
    'default': settings.MULTISCHEMA_DEFAULT_NAMESPACE,
}

def default_alias_handler(alias='default'):
    paths = [default_mapping.get(alias, alias)]
    
    if settings.MULTISCHEMA_APPEND_DEFAULT_NAMESPACE:
        paths.append(settings.MULTISCHEMA_DEFAULT_NAMESPACE)
    return paths




alias_handler = get_callable(settings.MUTLISCHEMA_ALIAS_HANDLER)

def create_namespace_if_not_exist(sender, connection, **kwargs):
    connected_alias = get_connection_alias(connection)
    if connected_alias == 'default': return
    
    try:
        ns = connected_alias and alias_handler(alias=connected_alias) or None
        if ns:
            cursor = connection.cursor()
            namespace.create(ns[0], cursor=cursor)
    except Exception, err:
        print 'Create namespace error', err
        
def switch_to_namespace_on_connect(sender, connection, **kwargs):
    connected_alias = get_connection_alias(connection)
    
    if connected_alias:
        logging.debug('Connection created to %s' % connected_alias)
        namespaces = alias_handler(alias=connected_alias)
        cursor = connection.cursor()
        namespace.switch_to(*namespaces, cursor=cursor)
