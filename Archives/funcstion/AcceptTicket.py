#! /usr/bin/env python
# coding=utf-8
from SM9gen import *
import sys

reload(sys)
import shutil
# sys.setdefaultencoding("utf-8")
import csc.csclxmls
import path
import traceback
import datetime

cfg = csc.csclxmls.node.cfgfile()

if cfg('/root/item[@key="Pid check"]').text:
    if not cfg.pidfilecheck():
        print cfg('/root/item[@key="Exit Error"]').text
        sys.exit(1)
try:

    # code starts here --------------------------------------------------------------------------------
    # path-ing settings.xml
    pth = path.path('settings.xml')
    cc = csc.csclxmls.node(pth)
    sm9_firefox_start()
    # login
    sm9_login()
    # choose nav
    sm9_navpanel(4)
    sm9_opensearch(2)
    queryname = cc('//item[@key="queryname"]').text
    directory = "C:\SM9automation\Incident\%s" % queryname
    archive = "C:\SM9automation\Archive"
    try:
        no = 1
        for dirs in os.listdir(directory):
            if os.path.isdir(directory + "\\" + dirs):
                if os.path.exists(directory + "\\" + dirs + ".lck"):
                    print str(dirs) + " is locked , next inm"
                else:
                    print "no lck: " + dirs + " , creating new lockfile to start work"
                    open(directory + "\\" + dirs + ".lck", 'w')
                    sm9_search_id(dirs)
                    sm9_accept("Accepted")

                    print 'Accepted'
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    # print str(currentdate)
                    # source =
                    print 'moving ' + dirs + " to archive"
                    print "moving " + str(directory + "\\" + dirs) + " to " + str(archive + "\\" + dirs + str(timestr))
                    os.rename(directory + "\\" + dirs, archive + "\\" + dirs + "_" + str(timestr))
                    time.sleep(2)
                    print 'deleting lck: ' + dirs
                    os.remove(directory + "\\" + dirs + ".lck")
                print str(no)
                no += 1
                print "going back to check folder"
                time.sleep(5)
    except:
        print "no folders, resetting"
        time.sleep(5)
except:
    print traceback.format_exc()
finally:
    if cfg('/root/item[@key="Pid check"]').text:
        if cfg.pidfilecheck():
            print cfg('/root/item[@key="Exit"]').text
            cfg.pidfile.unlink()
            sys.exit()
