from django.utils import unittest
from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
from django.db.models import Max
from django.db import connections

import random

class MultiSchemaTestCase(unittest.TestCase):
    def setUp(self):
        self.dbs = settings.DATABASES.keys()
        
        for db in self.dbs:
            if db not in ['default'] and db :
                call_command('createschema', db)
            call_command('syncdb', interactive=False, database=db, cursor=connections['default'].cursor(), verbosity=0)

    def testCreate(self):
        for i in range(10000):
            db = random.choice(self.dbs)
            user_id = (User.objects.using(db).aggregate(next_id=Max('pk'))['next_id'] or 0) + 1
            User.objects.using(db).create(username='{0}@{1}'.format(user_id, db))

    def testRead(self):
        for db in self.dbs:
            print 'testRead', db
            self.assertEqual(User.objects.using(db).exclude(username__icontains='@%s' % db).exists(), False)
