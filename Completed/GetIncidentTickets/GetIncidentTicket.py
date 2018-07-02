#! /usr/bin/env python
# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from SM9gen import *
import csc.csclxmls, path, traceback, firefoxdriver

timestr = time.strftime("%Y%m%d")
out = path.path('incident_get_%s.log' % timestr)
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
    out.write_bytes("Initiating Firefox")
    sm9_firefox_start()
    # login
    out.write_bytes("Starting Login Process ")
    sm9_login()
    # choose nav
    out.write_bytes("Open Fav and Dashboard")
    sm9_navpanel(1)

    # Query Select
    out.write_bytes("Selecting")
    sm9_favdash_query_select()

    sm9_navpanel(1)
    while 1:
        sm9_query_data_collection()
        firefoxdriver.driver.switch_to.default_content()
        UserInfo = WebDriverWait(firefoxdriver.driver, 10)
        UserInfo.until(ec.presence_of_element_located(
            (By.XPATH,
             '//div[@class=" x-panel x-panel-noborder"]/div/div[@class="x-panel-body x-panel-body-noheader x-panel-body-noborder x-border-layout-ct"]//button[contains(text(),"Refresh")]'))).click()
        time.sleep(2)


except:
    print traceback.format_exc()
finally:
    if cfg('/root/item[@key="Pid check"]').text:
        if cfg.pidfilecheck():
            print cfg('/root/item[@key="Exit"]').text
            cfg.pidfile.unlink()
            sys.exit()
