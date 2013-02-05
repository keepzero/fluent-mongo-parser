#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, "..")
import smtplib
from email.mime.text import MIMEText

from config import EMAIL_CONFIG

def send_mail(to_list, subject, content):
    """docstring for send_mail(to_list, subject, content)"""

    print "Sending email..."

    user = EMAIL_CONFIG['user'] if '@' not in EMAIL_CONFIG['user'] else EMAIL_CONFIG['user'][0:EMAIL_CONFIG['user'].index('@')]
    me = user + '<' + user + '@' + EMAIL_CONFIG['pfix'] + '>'
    msg = MIMEText(content, _charset = "utf8")
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    try:
        s = smtplib.SMTP()
        s.connect(EMAIL_CONFIG['host'])
        s.login(EMAIL_CONFIG['user'], EMAIL_CONFIG['pswd'])
        s.sendmail(me, to_list, msg.as_string())
        print "Sent done"
    except Exception, e:
        print str(e)


