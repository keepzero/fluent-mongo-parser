#!/usr/bin/env python

from config import MongoSource
from manager import PluginManager
from log import LogDocGenerator
import datetime

def main():

    # 1. load all plugins
    plugin_manager = PluginManager()

    # 2. get one or more mongodb collection 
    ms = MongoSource()
    collection = ms.get_collection("net-test", "ename_access")

    # 3. make a log_generator
    log_generator = LogDocGenerator(collection)

    # 4. use condition to get filtered logs
    #condition = {"host":"192.168.1.57"}
    now = datetime.datetime.now()
    start = now - datetime.timedelta(hours=8, minutes=10)
    end = now - datetime.timedelta(hours=8)
    condition = {"time":{"$gte":start, "$lt":end}}

    # 5. use keywords plugins to parse logs
    keywords = ['ip']
    for log_doc in log_generator.get_log_docs(condition):
        plugin_manager.call_method('process', args=log_doc, keywords=keywords)

    # 6. give a report
    plugin_manager.call_method('report', args={}, keywords=keywords)

if __name__ == '__main__':
    main()
