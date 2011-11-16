from django.db import connection, connections

import settings
from signals import pre_switch, post_switch, pre_create, post_create, pre_drop, post_drop

import logging
logger = logging.getLogger(__name__)


def switch_namespace(*namespaces, **kwargs):
    cursor = kwargs.pop('cursor', connection.cursor())
    pre_switch.send(sender=None)
    cursor.execute('SET search_path = %s;' % ','.join(['%s'] * len(namespaces)), namespaces)
    post_switch.send(sender=None)

def switch_to_default_namespace(cursor=None):
    switch_namespace(settings.MULTISCHEMA_DEFAULT_SCHEMA, cursor=cursor)

def create_namespace(namespace, cursor=None, check_existance=True):
    cursor = cursor or connection.cursor()
    pre_create.send(sender=None, namespace=namespace, cursor=cursor, requires_check=check_existance)
    if check_existance:
        if not check_namespace_existance(namespace, cursor=cursor):
            cursor.execute('CREATE SCHEMA "%s"' % namespace)
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=True, required_check=True)
        else:
            pass
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=False, required_check=True)
    else:
        try:
            cursor.execute('CREATE SCHEMA "%s"' % namespace)
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=True, required_check=False)
        except Exception, err:
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=False, required_check=False, error=err)

def list_namespaces(cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SELECT nspname as name from pg_namespace')
    namespaces = cursor.fetchall()
    return list(namespaces)

def check_namespace_existance(namespace, cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SELECT nspname as name from pg_namespace WHERE nspname=%s', [namespace])
    return bool(cursor.fetchone())

def get_current_search_path(cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SHOW search_path')
    paths = cursor.fetchall()
    return paths

def drop_namespace(namespace, requires_check=True, cursor=None):
    cursor = cursor or connection.cursor()
    exists = False
    pre_drop.send(sender=None, namespace=namespace, requires_check=requires_check, cursor=cursor)
    if requires_check:
        exists = check_namespace_existance(namespace, cursor=cursor)
    cursor.execute('DROP SCHEMA %s "%s" CASCADE' % (requires_check and 'IF EXISTS' or '', namespace))
    post_drop.send(sender=None, namespace=namespace, existed=True, cursor=cursor)

def rename_namespace(namespace_old, namespace_new, cursor=None):
    cursor = cursor or connection.cursor()
    pre_rename.send(sender=None, namespace_old=namespace_old, namespace_new=namespace_new, cursor=cursor)
    try:
        cursor.execute('ALTER SCHEMA "%s" RENAME TO "%s"' % (namespace_old, namespace_new))
        post_rename.send(sender=None, namespace_old=namespace_old, namespace_new=namespace_new, renamed=True)
        return True
    except:
        post_rename.send(sender=None, namespace_old=namespace_old, namespace_new=namespace_new, renamed=False)
    return False



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
