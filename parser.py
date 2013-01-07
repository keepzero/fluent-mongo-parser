#!/usr/bin/env python

from config import MongoSource
from manager import PluginManager
from log import LogDocGenerator

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
