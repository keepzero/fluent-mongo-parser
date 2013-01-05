#!/usr/bin/env python

from pymongo import MongoClient

CONFIG = {
    'host':  '192.168.1.211',
    'port':  27017,
    'user':  'mongo',
    'pswd':  'mongo',
}

class MongoSource:
    def __init__(self, host=None, port=27017, user="mongo", pswd="mongo"):
        if host:
            self.connection = MongoClient(host, port)
        else:
            self.connection = MongoClient(CONFIG['host'], CONFIG['port'])

    def get_db(self, dbname):
        """Get a mongo Database"""
        return self.connection[dbname]

    def get_database(self, dbname):
        return self.get_db(dbname)

    def get_collection(self, dbname, colname):
        return self.get_db(dbname)[colname]

    def get_client(self):
        return self.connection

    def get_connection(self):
        return self.get_client()
