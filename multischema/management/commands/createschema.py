from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections, transaction

from optparse import make_option

from multischema import namespace
from multischema import settings


class Command(BaseCommand):
    help = 'Create namespace'
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to synchronize. '
                'Defaults to the "default" database.'),
    )
    
    def handle(self, name, cursor=None, **options):
        if name in settings.MULTISCHEMA_ALIAS_EXCLUDE:
            raise CommandError('%s is on the exclude list' % name)
        cursor = cursor or connections[options.get('database', DEFAULT_DB_ALIAS)].cursor()
        
        if not namespace.exists(name):
            namespace.create(name, cursor=cursor)
            transaction.commit_unless_managed()
