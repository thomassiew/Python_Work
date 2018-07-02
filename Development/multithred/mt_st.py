#! /usr/bin/env python
# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import traceback
import datetime
import threading

class st_cls(threading.Thread, object):

    def __init__(self, parent):
        self.parent = parent
        threading.Thread.__init__(self)

    def __getattr__(self, item):
        if hasattr(self.parent, item):
            return getattr(self.parent, item)

    def run(self):
        while not self.end:
            self.sp.acquire()
            self.evt.wait()
            self.lk.acquire()
            print self.name, 'args', self.args
            print self.name, 'kwds', self.kwds
            print
            time.sleep(1)
            self.lk.release()
            self.sp.release()
            time.sleep(0.2)

