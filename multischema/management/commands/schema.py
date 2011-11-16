from django.core.management.base import BaseCommand, CommandError, handle_default_options
from django.core.management import call_command
from optparse import make_option
from optparse import OptionParser
from multischema.models import Schema

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def run_from_argv(self, argv):
        argv.pop(1)
        parser = OptionParser()
        parser.add_option('--schema', default='public')
        
        schema_opt = []
        for arg in argv:
            if '--schema' in arg:
                schema_opt.append(argv.pop(argv.index(arg)))
                break
        options, args = parser.parse_args(schema_opt)
        self.schema = options.__dict__.get('schema', 'public')
        
        self.cmd = argv[1]
        parser = self.create_parser(argv[0], argv[1])
        options, args = parser.parse_args(argv[2:])
        handle_default_options(options)
        self.execute(*args, **options.__dict__)
    
    def handle(self, *args, **kwargs):
        print 'Running %s schema %s' % (self.cmd, self.schema)
        
        from django.conf import settings
        if self.schema not in [getattr(settings, 'MULTISCHEMA_DEFAULT_SCHEMA', 'public'), None]:
            try:
                schema = Schema.objects.get(name=self.schema)
                with schema:
                    call_command(self.cmd, *args, **kwargs)
            except Schema.DoesNotExist:
                print 'Schema %s does not exist' % self.schema
        else:
            call_command(self.cmd, *args, **kwargs)
