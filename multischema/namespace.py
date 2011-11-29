from django.db import connection
from multischema import settings
from multischema.signals import pre_switch, post_switch, pre_create, post_create, pre_drop, post_drop, pre_rename, post_rename

import logging
logger = logging.getLogger(__name__)


def switch_to(*namespaces, **kwargs):
    if namespaces:
        cursor = kwargs.pop('cursor', connection.cursor())
        pre_switch.send(sender=None)
        logging.debug('Set search_path to %s' % ','.join(namespaces))
        cursor.execute('SET search_path = %s;' % ','.join(['%s'] * len(namespaces)), namespaces)
        post_switch.send(sender=None)

def switch_to_default(cursor=None):
    switch_to(settings.MULTISCHEMA_DEFAULT_SCHEMA, cursor=cursor)

def create(namespace, cursor=None, check_existance=True):
    cursor = cursor or connection.cursor()
    pre_create.send(sender=None, namespace=namespace, cursor=cursor, requires_check=check_existance)
    if check_existance:
        if not check_namespace_existance(namespace, cursor=cursor):
            cursor.execute('CREATE SCHEMA "%s"' % namespace)
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=True, required_check=True)
        else:
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=False, required_check=True)
    else:
        try:
            cursor.execute('CREATE SCHEMA "%s"' % namespace)
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=True, required_check=False)
        except Exception, err:
            post_create.send(sender=None, namespace=namespace, cursor=cursor, created=False, required_check=False, error=err)

def list(cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SELECT nspname as name from pg_namespace')
    namespaces = cursor.fetchall()
    return [ns[0] for ns in namespaces]

def check_namespace_existance(namespace, cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SELECT nspname as name from pg_namespace WHERE nspname=%s', [namespace])
    return bool(cursor.fetchone())

def get_current_search_path(cursor=None):
    cursor = cursor or connection.cursor()
    cursor.execute('SHOW search_path')
    paths = cursor.fetchall()
    return paths

def drop(namespace, requires_check=True, cursor=None):
    cursor = cursor or connection.cursor()
    exists = False
    pre_drop.send(sender=None, namespace=namespace, requires_check=requires_check, cursor=cursor)
    if requires_check:
        exists = check_namespace_existance(namespace, cursor=cursor)
    cursor.execute('DROP SCHEMA %s "%s" CASCADE' % (requires_check and 'IF EXISTS' or '', namespace))
    post_drop.send(sender=None, namespace=namespace, existed=True, cursor=cursor)

def rename(namespace_old, namespace_new, cursor=None):
    cursor = cursor or connection.cursor()
    pre_rename.send(sender=None, namespace_old=namespace_old, namespace_new=namespace_new, cursor=cursor)
    try:
        cursor.execute('ALTER SCHEMA "%s" RENAME TO "%s"' % (namespace_old, namespace_new))
        post_rename.send(sender=None, namespace_old=namespace_old, namespace_new=namespace_new, renamed=True)
        return True
    except:
        post_rename.send(sender=None, namespace_old=namespace_old, namespace_new=namespace_new, renamed=False)
    return False
