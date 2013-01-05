#!/usr/bin/env python

from manager import PluginManager
from config import MongoSource

class LogDocGenerator:
    def __init__(self, log_format, log_source):
        """docstring for __init__"""
        self.collection = log_source

    def get_log_docs(self):
        """docstring for get_log_docs"""
        return self.collection.find()

def main():
    plugin_manager = PluginManager()

    keywords = ['counter']

    ms = MongoSource()
    collection = ms.get_collection("net-test", "ename_access")
    log_generator = LogDocGenerator("", collection)
    for log_doc in log_generator.get_log_docs():
        plugin_manager.call_method('process', args=log_doc, keywords=keywords)
    plugin_manager.call_method('report', args={}, keywords=keywords)

if __name__ == '__main__':
    main()
