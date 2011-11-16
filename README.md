In this document, I call schemas as namespace since Postgresql "schema"s mean something else in a different type of database.



Single Connection
    * TODO


Multi Connection
    Creates a new database connection per namespace.  Should use external connection pooling or create a connection expiration function.
    
    In the example, all database entries point to the same database server. By default, MULTISCHEMA_ALIAS_MAP maps "default" to "public" and X to X, so abc.com would use namespace abc.com.

    1. Add a database entry to DATABASES for every namespace that you need to access.  (Example: abc.com, def.com, xyz.com)
    1.1 Change multischema settings if needed
    
    2. Sync database (Everything works like a multidatabase configuration using Django's multidb functions)
        1. python manage.py syncdb  (for default db)
        2. python manage.py syncdb --database abc.com (for abc.com)
        3. python manage.py syncdb --database def.com (for def.com)
        4. python manage.py syncdb --database xyz.com (for xyz.com)
    
    3. Usage
        * Model.objects.all() selects from "default" database using "public" namespace  (Normal non-multischema usage)
        * Model.objects.using("abc.com").all() selects from "abc.com" database using "abc.com" namespace
        * Model.objects.using("xyz.com").create(...) create object in "xyz.com" namespace
