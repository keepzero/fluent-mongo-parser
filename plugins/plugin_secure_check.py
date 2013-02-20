#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, "..")
import re

from libs.manager import Plugin
from libs.mail import send_mail

class SecureCheck(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['secure', 'check']
        self.result = {}

    def __process_doc(self, **kwargs):
        m = re.match("^(Accepted|Failed) password for ([a-z0-9]+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*", kwargs['message'])
        if m:
            #print m.group(1),m.group(2),m.group(3)
            if kwargs['host'] in self.result.keys():
                if m.group(3) in self.result[kwargs['host']][m.group(1)]:
                    self.result[kwargs['host']][m.group(1)][m.group(3)] += 1
                else:
                    self.result[kwargs['host']][m.group(1)][m.group(3)] = 1
            else:
                self.result[kwargs['host']] = {"Accepted":{}, "Failed":{}}

    def process(self, **kwargs):
        collection = kwargs['collection']
        cond = {}
        if 'condition' in kwargs:
            cond = kwargs['condition']

        condition = dict(
            cond, 
            ident = {"$in":['sshd']}, 
        )

        #print condition
        #print collection.database.name
        #print collection.database.command("distinct", "messages", key="ident", q=condition)

        # Do more HERE
        for log_doc in collection.find(condition):
            #print log_doc
            self.__process_doc(**log_doc)


    def report(self, **kwargs):
        #print self.result
        print "%-16s|%-16s|%8s|%-8s" % ("Host","IPs","Failed", "Accepted")
        print "---------------------------------------------------"

        for (host,action) in self.result.items():
            ips = list(set(action['Failed'].keys() + action['Accepted'].keys()))
            print "%-16s|%-16d|%8d|%8d" % (host,len(ips), sum(action['Failed'].values()), sum(action['Accepted'].values()))
            for ip in ips:
                fails = 0
                accepts = 0
                if action['Failed'].has_key(ip):
                    fails = action['Failed'][ip]
                if action['Accepted'].has_key(ip):
                    accepts = action['Accepted'][ip]
                print "%-16s|%-16s|%8d|%8d" % ("", ip, fails, accepts)
            print "-----------------------------------------------------"

