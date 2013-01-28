#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import sys
import re
from fluent import sender
from fluent import event

nginx_access = '(?P<host>[^ ]*) [^ ]* (?P<user>[^ ]*) \[(?P<time>[^\]]*)\] "(?P<method>\S+)(?: +(?P<path>[^ ]*) +\S*)?" (?P<code>[^ ]*) (?P<size>[^ ]*)(?: "(?P<referer>[^\"]*)" "(?P<agent>[^\"]*)")?'
nginx_error  = '(?P<time>[^\]]*) \[(?P<level>[^\]]*)\] (?P<pid>[^ ]*): *(?P<message>.*)'
syslog_message = '(?P<time>[^ ]* [^ ]* [^ ]*) (?P<host>[^ ]*) (?P<ident>[a-zA-Z0-9_\/\.\-]*)(?:\[(?P<pid>[0-9]+)\])?[^\:]*\: *(?P<message>.*)'
php_error = '\[(?P<time>[^\]]*)\] (?P<type>[^\]:]*): *(?P<message>.*)'
php_fpm = '\[(?P<time>[^\]]*)\] (?P<level>[^\]:]*): *(?P<message>.*)'
redis = '\[(?P<id>[^\]]*)\] (?P<time>[^ ]* [^ ]* [^ ]*) .? (?P<message>.*)'

typedict = {
    "access": nginx_access,
    "error": nginx_error,
    "syslog": syslog_message,
    "php_error": php_error,
    "php_fpm": php_fpm,
    "redis": redis
}

class LogGenerator:
    def __init__(self, logtype, doc_sender, logfiles):
        self.logtype = logtype
        self.logfiles = logfiles
        self.sender = doc_sender

        regex_str = typedict[logtype]
        self.key_list  = re.findall('\?P<(.*?)>', regex_str)
        self.regex = re.compile(regex_str)

    def make_doc(self, line):
        m = self.regex.search(line)
        if m:
            #print dict(zip(self.key_list, m.groups()))
            self.sender.send(dict(zip(self.key_list, m.groups())), self.logtype)

    def start(self):
        for file in self.logfiles:
            try:
                with open(file, 'r') as f:
                    for line in f: 
                        self.make_doc(line)
            except IOError, e:
                raise e
            except Exception, e:
                pass

class DocSender:
    def __init__(self, host, port, app, label):
        self.label = label
        sender.setup(app, host=host, port=port)

    def send(self, log, logtype):
        try:

            if logtype == "access":
                # Python 不支持数字格式的时区，直接去除时区，time.mktime 会获取本地时区
                t = time.strptime(log['time'].replace(" +0800",""), "%d/%b/%Y:%H:%M:%S")
            elif logtype == "error":
                t = time.strptime(log['time'], "%Y/%m/%d %H:%M:%S")
            elif logtype == "syslog":
                t = time.strptime(YEAR + " " + log['time'], "%Y %b %d %H:%M:%S")
            elif logtype == "php_error":
                t = time.strptime(log['time'], "%d-%b-%Y %H:%M:%S %Z")
            elif logtype == "php_fpm":
                t = time.strptime(log['time'], "%d-%b-%Y %H:%M:%S")
            elif logtype == "redis":
                t = time.strptime(YEAR + " " + log['time'], "%Y %d %b %H:%M:%S")
            else:
                exit()

            # delete time from log dict
            del log['time']

            # 如果系统时区和日志里面的时区不同，调整 time = int(xxx) +/- 多少时间
            event.Event(self.label, log, time = int(time.mktime(t)))  
        except Exception:
            print "send error:", log

def main():

    if len(sys.argv) < 6:
        print "Usage: python importer.py <host> <app> <label> access|error|syslog|php_error|php_fpm|redis [logfile.log ...]"
        exit()
    
    host     = sys.argv[1]
    port     = 24224
    app      = sys.argv[2]
    label    = sys.argv[3]
    logtype  = sys.argv[4]
    logfiles = sys.argv[5:]

    if logtype in ['syslog', 'redis']:
        global YEAR
        YEAR = raw_input("Enter Year of the log(2012/2013/...):")

    doc_sender = DocSender(host, port, app, label)

    log_generator = LogGenerator(logtype, doc_sender, logfiles)
    log_generator.start()

if __name__ == '__main__':
    main()
