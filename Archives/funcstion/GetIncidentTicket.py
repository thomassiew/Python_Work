#! /usr/bin/env python
# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from SM9func import *
import csc.csclxmls, path, traceback,firefoxdriver

cfg = csc.csclxmls.node.cfgfile()

if cfg('/root/item[@key="Pid check"]').text:
    if not cfg.pidfilecheck():
        print cfg('/root/item[@key="Exit Error"]').text
        sys.exit(1)
try:

    # code starts here --------------------------------------------------------------------------------
    # pathing settings.xml
    pth = path.path('settings.xml')
    cc = csc.csclxmls.node(pth)
    sm9_firefox_start()
    # login
    sm9_login()
    # choose nav
    sm9_navpanel(1)

    # Query Select
    sm9_favdash_query_select()
    # sm9_query_data_collection()
    # sm9_log_out()
    sm9_opensearch(2)
    directory = "C:\SM9automation\Incident\CUST"
    no = 1
    for dirs in os.listdir(directory):
        sm9_searchID(dirs)
        sm9_cancel()
        print str(no)
        no += 1

except:
    print traceback.format_exc()
finally:
    if cfg('/root/item[@key="Pid check"]').text:
        if cfg.pidfilecheck():
            print cfg('/root/item[@key="Exit"]').text
            cfg.pidfile.unlink()
            sys.exit()
