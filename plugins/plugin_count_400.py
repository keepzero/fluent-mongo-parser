#!/usr/bin/env python

from manager import Plugin

class CountHTTP400(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['counter', 'counter400']
        self.counter_400 = 0
        self.counter_total = 0

    def process(self, **kwargs):
        if 'code' in kwargs:
            self.counter_total += 1
            if kwargs['code'] == 400:
                self.counter_400 += 1

    def report(self, **kwargs):
        print '== HTTP code 400 counter =='
        print "HTTP 400 responses: %d" % self.counter_400
        print "All responses: %d" % self.counter_total
