from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections, transaction

from optparse import make_option

from multischema import namespace


class Command(BaseCommand):
    help = 'Create namespace'
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to synchronize. '
                'Defaults to the "default" database.'),
#        make_option('--confirm-drop', action='store', dest='confirmed',
#            default=False, help='Nominates a database to synchronize. '
#                'Defaults to the "default" database.'),
    )
    
    def handle(self, name, **options):
        cursor = connections[options.get('database', DEFAULT_DB_ALIAS)].cursor()
        namespace.drop(name, cursor=cursor)
        transaction.commit_unless_managed()
