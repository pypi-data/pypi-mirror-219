""" Superclass datasource for postgres/cockroach, mongodb, and sqlite """
class DataSource:
    """ abstracts initialization, connection, reading and writing """
    def __init__(self, database, table):
        """ common class variables used by subclasses """
        self.db_name     = database # name of database to use
        self.tbl_name    = table    # name of table/collection to use):
        self.connection  = None

    def write(self, data):
        """ pure virtual method which writes a new record into the datasource,
            and deletes any older records of the same type """

    def read(self, rectype):
        """  pure virtual method to reads one record from the database """
