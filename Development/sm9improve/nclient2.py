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
host = "bapaa485"
# host = '10.25.62.167'
# host = '10.25.39.153'
port = 60000
# port = 88
addr = (host, port)
st = time.time()

class _multiProcessing():


    def __init__(self):
        self.cp_count = multiprocessing.cpu_count() - 1
        self.mpqrl = multiprocessing.RLock()
        self.totalOK = multiprocessing.Value('i',0)

    def __call__(self):
        while 1:
            while len(multiprocessing.active_children()) < self.cp_count:
                process = _childProcess(self)
                process.start()
            time.sleep(0.2)

class _childProcess(multiprocessing.Process, object):


    def __init__(self, parent):
        self.parent = parent
        self.ct_count = 5
        multiprocessing.Process.__init__(self)

    def run(self):
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
        status = [self.pid, self.ident]
        ss = socket.socket(family=socketFamily, type=socketType)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            ss.connect(addr)
        except:
            status += ['mp connection refused']
            # st = ''
            # data = "x" * 1024
            # while len(data) == 1024:
        else:
            status += ['mp connected']
            try:
                st = ss.recv(1024)
            except:
                pass
            else:
                # except:
                #     continue
                # else:
                #     st += data
            # ss.shutdown(socket.SHUT_RDWR)
            # ss.close()
            # print 999, st
                if st:
                    ss = socket.socket(family=socketFamily, type=socketType)
                    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    ipa , ipx = st.split(':')
                    try:
                        ss.connect((ipa,int(ipx)))
                    except:
                        status += ['cp connection refused']
                    else:
                        status += ['cp connected']
                        try:
                            ss.send('thomas')
                        except:
                            status += ['connection send error']
                        # while 1:
                        try:
                            data = ss.recv(1024)
                        except:
                            pass
                        else:
                            # self.parent.parent.mpqrl.acquire()
                            # self.parent.parent.totalOK.value += 1
                            # if self.parent.parent.totalOK.value == 10000:
                            #     print 'success', str((10000)/(time.time() - st))
                            #     st = time.time()
                            #     self.parent.parent.totalOK.value = 0
                            # self.parent.parent.mpqrl.release()
                            status += ['*** %s ***' % (data)]
                            # break
        # self.parent.parent.mpqrl.acquire()
        print status
        # self.parent.parent.mpqrl.release()

if __name__ == '__main__':
    g = globals()
    start = str(datetime.datetime.today().isoformat())
    cfg = csc.csclxmls.node.cfgfile()
    # if cfg('/root/item[@key="Pid check"]').text:
    #     if not cfg.pidfilecheck():
    #         print cfg('/root/item[@key="Exit Error"]').text
    #         sys.exit(1)
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
     