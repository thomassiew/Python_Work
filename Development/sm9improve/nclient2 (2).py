#! /usr/bin/env python
#coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import path
import csv
import csc.csclxmls
import traceback
import datetime
import multiprocessing
import threading
import socket

socketFamily = socket.AF_INET
socketType = socket.SOCK_STREAM
# host = socket.gethostbyname(socket.gethostname())
host = '10.25.39.134'
port = 60000
addr = (host, port)
st = time.time()

class _multiProcessing():


    def __init__(self):
        self.cp_count = multiprocessing.cpu_count() - 1
        self.mprl = multiprocessing.RLock()
        self.totalOK = multiprocessing.Value('i',0)
        self.cp = {}

    def __call__(self):
        while 1:
            while len(multiprocessing.active_children()) < self.cp_count:
                process = _childProcess(self)
                process.start()
            time.sleep(0.2)

class _childProcess(multiprocessing.Process, object):


    def __init__(self, parent):
        self.parent = parent
        self.ct_count = 100
        multiprocessing.Process.__init__(self)

    def run(self):
        self.parent.mprl.acquire()
        if self.parent.cp.has_key('cp1'):
            self.parent.cp['cp1'] = self.pid
            self.cp_name = 'cp1'
        elif self.parent.cp.has_key('cp2'):
            self.parent.cp['cp2'] = self.pid
            self.cp_name = 'cp2'
        elif self.parent.cp.has_key('cp3'):
            self.parent.cp['cp3'] = self.pid
            self.cp_name = 'cp3'
        else:
            self.parent.cp['cp4'] = self.pid
            self.cp_name = 'cp4'
        self.parent.mprl.release()
        while 1:
            while threading.activeCount() <= self.ct_count:
                thread = _childThread(self)
                thread.start()
            time.sleep(0.2)

class _childThread(threading.Thread,object):


    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent

    def __getattr__(self, item):
        if hasattr(self.parent, item):
            return getattr(self.parent, item)

    def run(self):
        # global st
        status = [self.cp_name, self.ident]
        ss = socket.socket(family=socketFamily, type=socketType)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            ss.connect(addr)
        except:
            status += ['mp connection refused']
        else:
            # status += ['mp connected']
            st = ''
            data = 'x' * 1024
            while len(data) == 1024:
                try:
                    data = ss.recv(1024)
                except:
                    continue
                st += data
            try:
                ipa , ipx = st.split(':')
            except:
                pass
            else:
                try:
                    ss.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                try:
                    ss.close()
                except:
                    pass
                ss = socket.socket(family=socketFamily, type=socketType)
                ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    ss.connect((ipa,int(ipx)))
                except:
                    status += ['cp connection refused']
                else:
                    # status += ['cp connected']
                    try:
                        ss.send('thomas')
                    except:
                        status += ['connection send error']
                    st = ''
                    data = 'x' * 1024
                    while len(data) == 1024:
                        try:
                            data = ss.recv(1024)
                        except:
                            continue
                        st += data
                    status += ['*** %s ***' % (st)]
        # self.parent.parent.mprl.acquire()
        # print status
        # self.parent.parent.mprl.release()

if __name__ == '__main__':
    g = globals()
    start = str(datetime.datetime.today().isoformat())
    cfg = csc.csclxmls.node.cfgfile()
    if cfg('/root/item[@key="Pid check"]').text:
        if not cfg.pidfilecheck():
            print cfg('/root/item[@key="Exit Error"]').text
            sys.exit(1)
    try:
        var_list = cfg('//variables//item[@key="Variable"]/..')
        if not (isinstance(var_list, csc.csclxmls.nodelist)): var_list = [var_list]
        var_dt = {}
        for var in var_list:
            variable = var('./item[@key="Variable"]').text
            value_list = var('./item[@key="Value"]').text
            for value in str(value_list).splitlines():
                g[variable] = value
                var_dt[variable] = value
        s_message_fi_pth = path.path(s_message_fi)
        s_message = csc.csclxmls.node(s_message_fi_pth)
    except:
        pass
    try:
        df = _multiProcessing()
        df()
    except:
        print traceback.format_exc()
    finally:
        if cfg('/root/item[@key="Pid check"]').text:
            if cfg.pidfilecheck():
                print cfg('/root/item[@key="Exit"]').text
                cfg.pidfile.unlink()
        stop = str(datetime.datetime.today().isoformat())
        print 'SCRIPT START = %(start)s' % (g)
        print 'SCRIPT STOP  = %(stop)s' % (g)
        sys.exit()
     