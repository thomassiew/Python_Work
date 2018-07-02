#! /usr/bin/env python
# coding=utf-8
import SM9gen
import sys

reload(sys)
import shutil
# sys.setdefaultencoding("utf-8")
import csc.csclxmls
import path
import os , time

cfg = csc.csclxmls.node.cfgfile()

# if cfg('/root/item[@key="Pid check"]').text:
#     if not cfg.pidfilecheck():
#         print cfg('/root/item[@key="Exit Error"]').text
#         sys.exit(1)
# try:

# code starts here --------------------------------------------------------------------------------
# path-ing settings.xml
pth = path.path('settings.xml')
cc = csc.csclxmls.node(pth)
SM9gen.sm9_firefox_start()
# login
SM9gen.sm9_login()
# choose nav
SM9gen.sm9_navpanel(4)
SM9gen.sm9_opensearch(2)
queryname = cc('//item[@key="queryname"]').text
directory = "C:\SM9automation\Incident\%s" % queryname
archive = "C:\SM9automation\Archive"
print " Checking folder if any ID exist"
while 1:
    reload(SM9gen)
    if len(os.listdir(directory)) < 1:
        print "no folders, reset"
        time.sleep(5)

    else:
        no = 1
        for dirs in os.listdir(directory):
            print "ID Located"
            if os.path.isdir(directory + "\\" + dirs):
                if os.path.exists(directory + "\\" + dirs + ".lck"):
                    print str(dirs) + " is locked , next inm"
                else:
                    print "no lck: " + dirs + " , creating new lockfile to start work"
                    open(directory + "\\" + dirs + ".lck", 'w')
                    SM9gen.sm9_search_id(dirs)
                    # work starts here ----------------------------------------------
                    SM9gen.sm9_accept("Accepted")

                    print 'Accepted'

                    # works end here ---------------------------------------------------
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    # print str(currentdate)
                    # source =
                    print 'moving ' + dirs + " to archive"
                    print "moving " + str(directory + "\\" + dirs) + " to " + str(archive + "\\" + dirs + str(timestr))
                    os.rename(directory + "\\" + dirs, archive + "\\" + dirs + "_" + str(timestr))

                    print 'deleting lck: ' + dirs
                    os.remove(directory + "\\" + dirs + ".lck")
                print str(no)
                no += 1
                print "going back to check folder"
                time.sleep(5)  # except:
#     print traceback.format_exc()
# finally:
#     if cfg('/root/item[@key="Pid check"]').text:
#         if cfg.pidfilecheck():
#             print cfg('/root/item[@key="Exit"]').text
#             cfg.pidfile.unlink()
#             sys.exit()
