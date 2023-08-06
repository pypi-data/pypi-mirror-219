import uuid
import json

import psycopg2
import psycopg2.extras

from datasourcelib.datasource import DataSource

class PostgresDB(DataSource):
    """ PostgresDB(DataSource) is a subclass of DataSource 
            which overrides the read(data) -> json and 
            write(data) for postgresql database
    """
    def __init__(self, userpass, hostport, db_name, tbl_name):
        """ Accepts an existing client, or creates a new client"""
        super().__init__(db_name, tbl_name)
        self.connection = self.connect(userpass, hostport)

    def connect(self, userpass, hostport):
        """ override connect method """
        dsn = f'postgres://{userpass}@{hostport}/{self.db_name}'
        con = psycopg2.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor)
        with con.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.tbl_name} (id UUID \
                        PRIMARY KEY, rectype TEXT, recupdate TEXT, \
                        recvalid TEXT, recvalues JSONB)")
        con.commit()
        return con

    def write(self, data):
        """ override write """
        recid     = uuid.uuid4()
        rectype   = data['type']
        recupdate = data['updated']
        recvalid  = data['valid']
        recvalues = json.dumps(data['values']).replace("'",r"''")

        istring = f"INSERT INTO {self.tbl_name} (id , rectype, recupdate, \
            recvalid, recvalues) VALUES \
            ('{recid}', '{rectype}', '{recupdate}', '{recvalid}', '{recvalues}')"
        dstring = f"DELETE FROM {self.tbl_name} WHERE rectype='{rectype}' \
                        AND NOT id='{recid}'"
        with self.connection.cursor() as cur:
            cur.execute(istring)
            cur.execute(dstring)
        self.connection.commit()

    def read(self, rectype):
        """ override read """

        with self.connection.cursor() as cur:
            cur.execute(f"SELECT rectype, recupdate, recvalid, recvalues \
                        FROM {self.tbl_name} WHERE rectype='{rectype}'")
            rows = cur.fetchall()
            self.connection.commit()
            if len(rows) > 0:
                data = {}
                for row in rows:
                    data['type']    = row['rectype']
                    data['updated'] = row['recupdate']
                    data['valid']   = row['recvalid']
                    data['values']  = row['recvalues']
            else:
                data = None
        return data

    def close(self):
        self.connection.close()
