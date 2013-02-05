#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime

from libs.manager import PluginManager
from libs.log import LogDocGenerator
import config

# 1. load all plugins
plugin_manager = PluginManager()

def parse(collection, condition, keywords):
    """docstring for parser"""
    log_generator = LogDocGenerator(collection)
    for log_doc in log_generator.get_log_docs(condition):
        plugin_manager.call_method('process', args = log_doc, keywords = keywords)

def report(keywords):
    """docstring for report"""
    plugin_manager.call_method('report', args={}, keywords=keywords)

def main():

    # 2. mongodb authenticate
    conn = config.get_connection()
    db = conn["admin"]
    db.authenticate("root","password")

    # 3. make condition to get filtered logs
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(days=0, hours=2, minutes=30)
    condition = {"time":{"$gte":start}}

    # 4. define keywords plugins to parse logs
    keywords = ['nginx']

    # 5. parse collections and report
    collections = []
    collections.append(conn["host1"]["nginx_error"])
    collections.append(conn["host2"]["nginx_error"])
    for coll in collections:
        parse(coll, condition, keywords)
    report(keywords)


if __name__ == '__main__':
    main()
