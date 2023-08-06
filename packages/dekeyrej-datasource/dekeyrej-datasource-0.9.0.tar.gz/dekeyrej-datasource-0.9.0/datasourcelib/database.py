from datasourcelib.mongodb    import MongoDB
from datasourcelib.postgresdb import PostgresDB
from datasourcelib.sqlitedb   import SQLiteDB

class DatabaseConnectionTypeError(Exception):
    pass

class DatabaseConnectionError(Exception):
    pass

class Database():
    """ 
    Class description 
    param: type - one of 'postgres', 'mongo', or 'sqlite'
    param: params - dict containing {user, pass, host, port, dbn, tbl}, {host, port, dbn, tbl} or {db_path, dbn, tbl}
    """
    def __init__(self, type, params):
        self._db_type = type
        self._db_params = params
        self._db = self.connect()

    def connect(self):
        if self._db_type == 'postgres':
            return self.connect_postgres()
        elif self._db_type == 'mongo':
            return self.connect_mongo()
        elif self._db_type == 'sqlite':
            return self.connect_sqlite()
        else:
            raise DatabaseConnectionTypeError

    def connect_postgres(self): # postgresql or cockroachdb
        """ connect to a particular postgres """
        unp = f"{self._db_params['user']}:{self._db_params['pass']}"
        hnp = f"{self._db_params['host']}:{self._db_params['port']}"
        dbn = self._db_params['db_name']
        tbl = self._db_params['tbl_name']
        return PostgresDB(unp, hnp, dbn, tbl)

    def connect_mongo(self): # mongodb
        """ connect to a particular postgres """
        host = self._db_params['host']
        port = self._db_params['port']
        dbn = self._db_params['db_name']
        tbl = self._db_params['tbl_name']
        return MongoDB(host, port, dbn, tbl)

    def connect_sqlite(self): # sqlite
        """ connect to a particular postgres """
        path = self._db_params['db_path'] 
        dbn = self._db_params['db_name']
        tbl = self._db_params['tbl_name']
        return SQLiteDB(path, dbn, tbl)

    def read(self, type):
        return self._db.read(type)

    def write(self, data):
        self._db.write(data)

    def close(self):
        self._db.close()
