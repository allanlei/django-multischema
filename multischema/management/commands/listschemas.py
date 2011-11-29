from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections

from optparse import make_option

from multischema import namespace


class Command(BaseCommand):
    help = 'Create namespace'
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to synchronize. '
                'Defaults to the "default" database.'),
    )
    
    def handle(self, **options):
        cursor = connections[options.get('database', DEFAULT_DB_ALIAS)].cursor()
        for ns in namespace.list(cursor=cursor):
            self.stdout.write(ns + '\n')
