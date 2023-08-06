import json
import uuid

import sqlite3

from datasourcelib.datasource import DataSource

class SQLiteDB(DataSource):
    """ SQLiteDB(DataSource) is a subclass of DataSource 
            which overrides the read(data) -> json and 
            write(data) for sqlite database
    """
    def __init__(self, path, db_name, tbl_name):
        """ Accepts an existing client, or creates a new client"""
        super().__init__(db_name, tbl_name)
        self.connection = self.connect(path)

    def connect(self, path):
        """ override connect method """
        con = sqlite3.connect(path) # creates it if it doesn't exist
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tbl_name} (id UUID PRIMARY KEY,
                        rectype STRING, recupdate STRING,
                        recvalid STRING, recvalues JSON)""")
        con.commit()
        return con

    def write(self, data):
        """ override write """
        recid     = uuid.uuid4()
        rectype   = data['type']
        recupdate = data['updated']
        recvalid  = data['valid']
        recvalues = json.dumps(data['values']).replace("'",r"''")
        istring = f"INSERT INTO {self.tbl_name} (id , rectype, recupdate, recvalid, recvalues) \
            VALUES ('{recid}', '{rectype}', '{recupdate}', '{recvalid}', '{recvalues}')"
        dstring = f"DELETE FROM {self.tbl_name} WHERE rectype='{rectype}' AND NOT id='{recid}'"
        cur = self.connection.cursor()
        # with self.connection.cursor() as cur:  ## this does not work with SQLite ?!?
        cur.execute(istring)
        cur.execute(dstring)
        self.connection.commit()

    def read(self, rectype):
        """ override read """
        cur = self.connection.cursor()
        # with self.connection.cursor() as cur: ## this does not work with SQLite ?!?
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
                data['values']  = json.loads(row['recvalues'])
        else:
            data = None
        return data

    def close(self):
        self.connection.close()
