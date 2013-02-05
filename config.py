#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

MONGO_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'user': 'root',
    'pswd': 'password',
}

EMAIL_CONFIG = {
    'host': "smtp.example.com",
    'user': "user@example.com",
    'pswd': "password",
    'pfix': "example.com"
}

def get_connection():
    """
    Simple method to get mongo connection.
       You may need to auth with mongo.
    """
    return MongoClient(MONGO_CONFIG['host'], MONGO_CONFIG['port'])

class MongoSource:
    def __init__(self, host="127.0.0.1", port=27017, user="", pswd=""):
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
