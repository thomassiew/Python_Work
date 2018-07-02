#! /usr/bin/env python
# coding=utf-8

import sys,shutil,os,filelock

reload(sys)
sys.setdefaultencoding("utf-8")
import SM9_V2
import csc.csclxmls, path, traceback, time, firefoxdriver

cfg = csc.csclxmls.node.cfgfile()
sm9 = SM9_V2.sm9_general(str(os.getpid()))
creddir = path.path('CREDS')
while True:
    if cfg('/root/item[@key="Pid check"]').text:
        if not cfg.pidfilecheck():
            print cfg('/root/item[@key="Exit Error"]').text
            sys.exit(1)
    try:
        sm9 = SM9_V2.sm9_general(str(os.getpid()))
        # pathing settings.xml

        pth = path.path('XML/settings.xml')
        cc = csc.csclxmls.node(pth)
        sm9.sm9_logging("Initiating Firefox")
        sm9.sm9_firefox_start()
        # login
        sm9.sm9_logging("Starting Login Process ")
        try:
            for creds in os.listdir(creddir):
                modixml = os.path.basename(creds)
                a, b = modixml.split(".")
                fl = filelock.FileLock(creddir + "\\" + a + ".lck", .5)
                if not os.path.exists(creddir + "\\" + a + ".lck"):

                    # get cred name
                    sm9.sm9_logging("CREDS :" + a + " not lck: " + " , creating lck")
                    fl.acquire(timeout=3)
                    sm9.sm9_login(creds)
                    break
                else:
                    sm9.sm9_logging("Login Failed , retrying with another creds")
        except:
            sm9.sm9_logging("All creds are used , retrying in 100 seconds , send mail")
            time.sleep(100)
            continue
        # choose nav
        sm9.sm9_logging("Open Fav and Dashboard")
        sm9.sm9_navpanel(1)
        sm9.sm9_logging("Selecting")
        sm9.sm9_favdash_query_select()

        sm9.sm9_navpanel(1)
        while 1:
            sm9.sm9_query_data_collection()
            firefoxdriver.driver.switch_to.default_content()
            sm9.refresh()
            time.sleep(2)

    except:
        sm9.sm9_logging(traceback.format_exc())
    finally:
        try:
            sm9.sm9_log_out()
        except:
            sm9.sm9_logging("Cant logout, proceeding to close and restart")
        finally:
            sm9.wait_click('//a[@id="loginAgain"]',20)
            #firefoxdriver.driver.close()
            #firefoxdriver.driver.quit()
            sm9.sm9_logging("Quitting Firefox , removing geckodriver and attempt restart in 15 secs")
            time.sleep(15)

            if cfg('/root/item[@key="Pid check"]').text:
                if cfg.pidfilecheck():
                    print cfg('/root/item[@key="Exit"]').text
                    cfg.pidfile.unlink()
                   # sys.exit()