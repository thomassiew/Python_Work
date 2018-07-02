#! /usr/bin/env python
#coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import traceback
import datetime
import threading
import mt_st
import Queue

class mt_cls():

    def __init__(self, *args, **kwds):
        self.args = list(args)
        self.kwds = dict(kwds)
        self.sp = threading.BoundedSemaphore(5)
        self.lk = threading.RLock()
        self.evt = threading.Event()
        self.end = False
        self.qq = Queue.Queue(2)

    def __call__(self, *args, **kwargs):
        reload(mt_st)
        print self, 'args', self.args
        print self, 'kwds', self.kwds
        print
        self.args += [7,8,9,10,11,12]
        self.kwds.update({'e':4,'f':5,'g':6,'h':7})
        self.evt.set()
        print self, 'args', self.args
        print self, 'kwds', self.kwds
        print
        time.sleep(1)
        thread = mt_st.st_cls(self)
        thread.start()
        thread.join()
