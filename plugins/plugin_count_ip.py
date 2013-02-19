#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, "..")

from libs.manager import Plugin

class CountIPNew(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['counter', 'ip']
        self.total_ip = 0
        self.ip_dict = {}

    def __process_doc(self, **kwargs):
        if 'host' in kwargs:
            if self.ip_dict.has_key(kwargs['host']):
                self.ip_dict[kwargs['host']] += 1
            else:
                self.ip_dict[kwargs['host']] = 1
                self.total_ip += 1

    def process(self, **kwargs):
        collection = kwargs['collection']
        condition = {}
        if 'condition' in kwargs:
            condition = kwargs['condition']

        # Do more HERE
        for log_doc in collection.find(condition):
            self.__process_doc(**log_doc)


    def report(self, **kwargs):
        print '==  IP counter =='
        print "HTTP IPs: %d" % self.total_ip
        for ip in self.ip_dict.keys():
            print "%s: %d" % (ip, self.ip_dict[ip])

