#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, "..")

from libs.manager import Plugin
from bson.code import Code

class CountIPNew(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['counter', 'ip']
        self.result = {}

    def process(self, **kwargs):
        collection = kwargs['collection']
        condition = {}
        if 'condition' in kwargs:
            condition = kwargs['condition']

        reducer = Code("""
                    function(curr,result){
                      result.count++;
                    }
                    """)
        
        host_result = collection.group(
                key = {"host":1},
                condition = condition,
                initial = {"count":0},
                reduce = reducer)

        self.result[collection.name] = host_result
        
        # mongo shell command
        #db.runCommand({group:{ ns:"www_ename_cn_access", key:{host:1}, $reduce:function(curr,result){result.times += 1}, initial:{"times":0}}})
        #db.news_ename_cn_access.group({key:{host:1},reduce:function(curr,result){result.times += 1;},initial:{times:0}})

    def report(self, **kwargs):
        print '==  IP counter =='
        print self.result

