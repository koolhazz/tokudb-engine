#!/usr/bin/env python

import sys

def main():
    print "# generated by tokudb_upsert_int.py"
    print "source include/have_tokudb.inc;"
    print "source include/have_innodb.inc;"
    print "set default_storage_engine='tokudb';"
    print "disable_warnings;"
    print "drop table if exists tt, ti;"
    print "enable_warnings;"

    print "set tokudb_enable_fast_update=1;"
    print "set tokudb_disable_slow_update=1;"

    for t in [ 'tinyint', 'smallint', 'mediumint', 'int', 'bigint' ]:
        for u in [ '', 'unsigned' ]:
            for n in [ 'null', 'not null' ]:
                test_upsert_int(t, u, n)
    return 0

def test_upsert_int(t, u, n):
    print "create table tt ("
    print "    id %s %s %s primary key," % (t, u, n)
    if n == 'not null': n += ' default 0'
    print "    x %s %s %s," % (t, u, n)
    print "    y %s %s %s," % (t, u, n)
    print "    z %s %s %s," % (t, u, n)
    print "    a char(32), aa varchar(32)"
    print ");"
    print "insert noar into tt (id) values (1),(2),(3) on duplicate key update x=0;"
    print "insert noar into tt (id) values (1) on duplicate key update y=0,z=42;"
    print "insert noar into tt (id) values (1) on duplicate key update y=y+1,z=z+100;"
    print "insert noar into tt (id) values (1) on duplicate key update y=y-1;"
    print "insert noar into tt (id) values (1) on duplicate key update z=z-100;"

    print "create table ti like tt;"
    print "alter table ti engine=innodb;"
    print "insert noar into ti (id) values (1),(2),(3) on duplicate key update x=0;"
    print "insert noar into ti (id) values (1) on duplicate key update y=0,z=42;"
    print "insert noar into ti (id) values (1) on duplicate key update y=y+1,z=z+100;"
    print "insert noar into ti (id) values (1) on duplicate key update y=y-1;"
    print "insert noar into ti (id) values (1) on duplicate key update z=z-100;"

    print "let $diff_tables = test.tt, test.ti;"
    print "source include/diff_tables.inc;"

    print "drop table tt, ti;"

sys.exit(main())