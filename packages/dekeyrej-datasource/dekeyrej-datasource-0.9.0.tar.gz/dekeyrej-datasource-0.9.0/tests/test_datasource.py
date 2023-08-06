""" test reading from three database types """
import time
from datasourcelib      import Database

# sqlite_params =                                                     {"db_path": 'matrix.db', "db_name": 'matrix', "tbl_name": 'feed'}
# mongo_params =                                          {"host": 'localhost', "port": 27127, "db_name": 'matrix', "tbl_name": 'feed'}
# pg_params =     {"user": 'postgres', "pass": 'password', "host": 'localhost', "port":  5432, "db_name": 'matrix', "tbl_name": 'feed'}

    # dba =   Database('sqlite',   sqlite_params)  # local dev ~ 15ms
    # dba =   Database('postgres', pg_params)  # kubegres ~50ms
    # dba =   Database('postgres', cr_params)  # CockroachDB ~175ms
    # dba =   Database('mongo',    mongo_params)  # NOT WORKING YET

rectypes = ['Calendar', 'Family', 'Moon', 'Weather', 'MLB']

# test sqlite
def test_sqllite_read():
    t1 = time.monotonic()
    sqlite_params = {"db_path": 'matrix.db', "db_name": 'matrix', "tbl_name": 'feed'}
    dba = Database('sqlite', sqlite_params)  # local dev ~ 15ms

    for i in range(0,10):
        for rt in rectypes:
            data = dba.read(rt)
    dba.close()
    print(f'run time: {(time.monotonic() - t1) * 1000} milliseconds')

# test postgres (kubegres)
# def test_postgres_read():
#     t1 = time.monotonic()
#     pg_params =     {"user": 'postgres', "pass": 'password', "host": 'localhost', "port":  5432, "db_name": 'matrix', "tbl_name": 'feed'}
#     dba =   Database('postgres', pg_params)
#
#     for i in range(0,10):
#         for rt in rectypes:
#             data = dba.read(rt)
#     dba.close()
#     print(f'run time: {(time.monotonic() - t1) * 1000} milliseconds')
