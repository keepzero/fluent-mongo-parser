#!/usr/bin/env python

from pymongo import MongoClient

CONFIG = {
    'host':  '192.168.10.202',
    'port':  27017,
    'user':  'root',
    'pswd':  'password',
}

def get_connection():
    """
    Simple method to get mongo connection.
       You may need to auth with mongo.
    """
    return MongoClient(CONFIG['host'], CONFIG['port'])

class MongoSource:
    def __init__(self, host="127.0.0.1", port=27017, user="mongo", pswd="mongo"):
        self.connection = MongoClient(host, port)
        self.connection["admin"].authenticate(user, pswd)

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
