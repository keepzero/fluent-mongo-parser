#!/usr/bin/env python

from manager import PluginManager
from log import LogDocGenerator
import config
import datetime

def main():

    # 1. load all plugins
    plugin_manager = PluginManager()

    # 2. get one or more mongodb collection 
    conn = config.get_connection()
    collection = conn["com-test"]["www_ename_com_access"]

    # 3. make a log_generator
    log_generator = LogDocGenerator(collection)

    # 4. use condition to get filtered logs
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(days=2, minutes=30)
    end = now
    condition = {"time":{"$gte":start, "$lt":end}}

    # 5. use keywords plugins to parse logs
    keywords = ['ip']
    for log_doc in log_generator.get_log_docs(condition):
        plugin_manager.call_method('process', args=log_doc, keywords=keywords)

    # 6. give a report
    plugin_manager.call_method('report', args={}, keywords=keywords)

if __name__ == '__main__':
    main()
