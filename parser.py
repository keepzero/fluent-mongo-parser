#!/usr/bin/env python

from manager import PluginManager
from config import MongoSource

class LogDocGenerator:
    def __init__(self, log_source):
        """docstring for __init__"""
        self.collection = log_source

    def get_log_docs(self, condition={}):
        """docstring for get_log_docs"""
        if not condition:
            return self.collection.find()
        else:
            return self.collection.find(condition)


def main():
    plugin_manager = PluginManager()

    #keywords = ['counter', 'ip']
    #keywords = ['counter']
    keywords = ['ip']

    ms = MongoSource()
    collection = ms.get_collection("net-test", "ename_access")
    log_generator = LogDocGenerator(collection)

    #condition = {"host":"192.168.1.57"}
    condition = {}
    for log_doc in log_generator.get_log_docs(condition):
        plugin_manager.call_method('process', args=log_doc, keywords=keywords)
    plugin_manager.call_method('report', args={}, keywords=keywords)

if __name__ == '__main__':
    main()
