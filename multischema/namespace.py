from django.db import connection
from multischema import settings
from multischema.signals import pre_switch, post_switch, pre_create, post_create, pre_drop, post_drop, pre_rename, post_rename

import logging
logger = logging.getLogger(__name__)


def switch_to(ns, cursor=None, append_default=settings.MUTLISCHEMA_DEFAULT_NAMESPACE_FALLBACK):
    cursor = cursor or connection.cursor()
    search_path = [ns]
    if append_default:
        search_path.append(settings.MULTISCHEMA_DEFAULT_NAMESPACE)

    pre_switch.send(sender=None, namespace=ns, search_path=search_path, cursor=cursor)
    cursor.execute('SET search_path = %s;' % ','.join(['%s'] * len(search_path)), search_path)
    post_switch.send(sender=None, namespace=ns, search_path=search_path, cursor=cursor)

def switch_to_default(cursor=None):
    switch_to(settings.MULTISCHEMA_DEFAULT_SCHEMA, cursor=cursor)

def create(namespace, cursor=None):
    cursor = cursor or connection.cursor()
    pre_create.send(sender=None, namespace=namespace, cursor=cursor)
    cursor.execute('CREATE SCHEMA "%s"' % namespace)
    post_create.send(sender=None, namespace=namespace, cursor=cursor, created=True)

def list(cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SELECT nspname as name from pg_namespace')
    namespaces = cursor.fetchall()
    return [ns[0] for ns in namespaces]

def check_namespace_existance(*args, **kwargs):
    return exists(*args, **kwargs)

def exists(namespace, cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SELECT nspname as name from pg_namespace WHERE nspname=%s', [namespace])
    return bool(cursor.fetchone())
    
def get_current_search_path(cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SHOW search_path')
    paths = cursor.fetchall()
    return paths

def drop(namespace, silent=True, cursor=None):
    cursor = cursor or connection.cursor()
    exists = False
    pre_drop.send(sender=None, namespace=namespace, cursor=cursor, silent=silent)
    if silent:
        cursor.execute('DROP SCHEMA IF EXISTS "%s" CASCADE' % namespace)
    else:
        cursor.execute('DROP SCHEMA "%s" CASCADE' % namespace)
    post_drop.send(sender=None, namespace=namespace, cursor=cursor, silent=silent)

def rename(namespace_old, namespace_new, cursor=None):
    cursor = cursor or connection.cursor()
    pre_rename.send(sender=None, from_namespace=namespace_old, to_namespace=namespace_new, cursor=cursor)
    cursor.execute('ALTER SCHEMA "%s" RENAME TO "%s"' % (namespace_old, namespace_new))
    post_rename.send(sender=None, from_namespace=namespace_old, to_namespace=namespace_new, cursor=cursor)
