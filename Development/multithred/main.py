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
import mt_mt

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
        while 1:
            reload(mt_mt)
            args = [1,2,3,4,5,6]
            kwds = {'a':1,'b':2,'c':3}
            df = mt_mt.mt_cls(*args, **kwds)
            df()
            time.sleep(1)
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
     