#!/usr/bin/env python

class LogDocGenerator:
    def __init__(self, log_source=None):
        """docstring for __init__"""
        self.collection = log_source if log_source else None

    def get_log_docs(self, condition={}):
        """docstring for get_log_docs"""
        if not condition:
            return self.collection.find()
        else:
            return self.collection.find(condition)

    def set_log_source(self, log_source):
        self.collection = log_source
