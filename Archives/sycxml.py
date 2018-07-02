#! /usr/bin/env python
# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import path
import csv
import csc.csclxmls
import traceback

cfg = csc.csclxmls.node.cfgfile()
if cfg('/root/item[@key="Pid check"]').text:
    if not cfg.pidfilecheck():
        print cfg('/root/item[@key="Exit Error"]').text
        sys.exit(1)
try:
   pass
except:
    print traceback.format_exc()
finally:
    if cfg('/root/item[@key="Pid check"]').text:
        if cfg.pidfilecheck():
            print cfg('/root/item[@key="Exit"]').text
            cfg.pidfile.unlink()
            sys.exit()
