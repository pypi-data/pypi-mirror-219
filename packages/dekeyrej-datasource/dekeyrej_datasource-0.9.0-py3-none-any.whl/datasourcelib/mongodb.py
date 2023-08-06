from pymongo import MongoClient

from datasourcelib.datasource import DataSource

class MongoDB(DataSource):
    """ Overrides initalization/connection, write and read """
    def __init__(self, host, port, db_name, tbl_name):
        super().__init__(db_name, tbl_name)
        self.connection = self.connect(host, port)

    def connect(self, host, port):
        connection = MongoClient(host, port)
        self.database   = connection[self.db_name]
        self.collection = self.database[self.tbl_name]
        return connection

    def write(self, data):
        """ overides superclass write() for MongoDB """
        ecks = self.collection.insert_one(data)
        if ecks.acknowledged is True:
            # print(f'Inserted 1 record of {size} bytes at {now_string()}')
            # print(f'Inserted 1 record at {now_string()}')
            delquery = {'_id': {'$lt': ecks.inserted_id }, 'type' : data['type'] }
            self.collection.delete_many(delquery)
            # why = self.collection.delete_many(delquery)
            # self.log('{} record(s) deleted.'.format(why.deleted_count))

    def read(self, rectype):
        """ overides superclass read() for MongoDB """
        result = self.collection.find_one(
            filter={ 'type': rectype },
            projection={ '_id': 0 },
            sort=list({ '_id': -1 }.items()),
            limit=1
        )
        return result  # either a dict or None

    # def now_string(self):
    #     """ return formatted string of 'now' """
    #     return arrow.now().format('DD/MM/YYYY HH:mm:ss')

    def close(self):
        self.connection.close()
