#! /usr/bin/env python
# coding=utf-8

import sys,shutil

reload(sys)
sys.setdefaultencoding("utf-8")
import SM9_V2
import csc.csclxmls, path, traceback, time, firefoxdriver

cfg = csc.csclxmls.node.cfgfile()
while True:
    if cfg('/root/item[@key="Pid check"]').text:
        if not cfg.pidfilecheck():
            print cfg('/root/item[@key="Exit Error"]').text
            sys.exit(1)
    try:
        waiting = SM9_V2.sm9_wait()
        # pathing settings.xml

        pth = path.path('XML/settings.xml')
        cc = csc.csclxmls.node(pth)
        SM9_V2.sm9_logging("Initiating Firefox")
        SM9_V2.sm9_firefox_start()
        # login
        SM9_V2.sm9_logging("Starting Login Process ")
        SM9_V2.sm9_login()
        # choose nav
        SM9_V2.sm9_logging("Open Fav and Dashboard")
        SM9_V2.sm9_navpanel(1)
        SM9_V2.sm9_logging("Selecting")
        SM9_V2.sm9_favdash_query_select()

        SM9_V2.sm9_navpanel(1)
        while 1:
            SM9_V2.sm9_query_data_collection()
            firefoxdriver.driver.switch_to.default_content()
            button = SM9_V2.sm9_buttons()
            button.refresh()
            time.sleep(2)

    except:
        SM9_V2.sm9_logging(traceback.format_exc())
    finally:
        try:
            SM9_V2.sm9_log_out()
        except:
            SM9_V2.sm9_logging("Cant logout, proceeding to close and restart")
        finally:
            waiting.wait_click('//a[@id="loginAgain"]',20)
            #firefoxdriver.driver.close()
            #firefoxdriver.driver.quit()
            SM9_V2.sm9_logging("Quitting Firefox , removing geckodriver and attempt restart in 15 secs")
            time.sleep(15)

            if cfg('/root/item[@key="Pid check"]').text:
                if cfg.pidfilecheck():
                    print cfg('/root/item[@key="Exit"]').text
                    cfg.pidfile.unlink()
                   # sys.exit()