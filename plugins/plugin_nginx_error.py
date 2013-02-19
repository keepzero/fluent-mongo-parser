#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, "..")
import re

from libs.manager import Plugin

class NginxError(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['nginx', 'error']
        self.total_line = 0
        self.level_dict = {"error": 0, "notice": 0, "info": 0, "alert": 0}
        self.client_dict = {}

    def process(self, **kwargs):
        """docstring for process"""
        #self.total_line += 1
        collection = kwargs['collection']
        condition = {}
        if 'condition' in kwargs:
            condition = kwargs['condition']

        # do more query HERE
        for log_doc in collection.find(condition):
            try:
                self.level_dict[log_doc['level']] += 1
                message = log_doc['message']
                m = re.match(".*client: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*", message)
                if m:
                    if m.group(1) in self.client_dict:
                        self.client_dict[m.group(1)] += 1
                    else:
                        self.client_dict[m.group(1)] = 1
            except KeyError:
                pass
            except:
                raise


    def report(self, **kwargs):
        """docstring for report"""
        print "====== Nginx Error ======"
        #print "Nginx total error line: %d" % self.total_line
        for level in self.level_dict.keys():
            print "%s: %d" % (level, self.level_dict[level])
        clients = sorted(self.client_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse = True)
        for client in clients:
            if client[1] > 50:
                print "%s: %d" % (client[0], client[1])
