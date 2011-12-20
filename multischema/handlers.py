from django.core.urlresolvers import get_callable
from django.db import transaction

from multischema import settings
from multischema import namespace
from multischema.utils import get_connection_alias

import logging
logger = logging.getLogger(__name__)
alias_lookup = get_callable(settings.MULTISCHEMA_REVERSE_LOOKUP_HANDLER)


def create_namespace_if_not_exist(sender, connection, **kwargs):
    connected_alias = get_connection_alias(connection)
    
    if connected_alias and connected_alias not in settings.MULTISCHEMA_ALIAS_EXCLUDE:
        ns = alias_lookup(connected_alias)
        
        if ns and not namespace.exists(ns):
            cursor = connection.cursor()
            
            with transaction.commit_on_success(using=connected_alias):
                namespace.create(ns, cursor=cursor)
        
def switch_to_namespace_on_connect(sender, connection, **kwargs):
    connected_alias = get_connection_alias(connection)
    
    if connected_alias and connected_alias not in settings.MULTISCHEMA_ALIAS_EXCLUDE:
        ns = alias_lookup(connected_alias)
        if ns:
            cursor = connection.cursor()
            with transaction.commit_on_success(using=connected_alias):
                namespace.switch_to(ns, cursor=cursor)
