#! /usr/bin/env python
# coding=utf-8

import sys
import csc.csclxmls
import path
import time
import os
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver
from cndmini import loginsm9, waitpageload, selectquery, CNDACCEPT
from selenium.common.exceptions import NoSuchElementException


def start(username, password):
    # configuring and firefox profile preferences
    storetype = "application/octet-stream;application/zip;application/x-troff-man;application/x-zip-compressed;application/msword"
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 1)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", storetype)
    fp.update_preferences()
    # setting website and access link through browser
    weblink = 'https://smweb.telekom.de/sm-prod/index.do?lang=en'
    browser = webdriver.Firefox(firefox_profile=fp)
    browser.get(weblink)
    # username and password to login sm9
    loginsm9(username, password, browser)
    # Loading Home Page of SM9 and load dashboard
    waitpageload('ROOT/Favorites and Dashboards', browser)
    # SM9 Loaded and codes starts here
    # -----------------------------------------------------------------------------------------------
    # Open Change searcher
    selectquery(2, "SEL_EVT_ACCEPTonly", browser)
    # selectquery(2, "CUST", browser)

    while True:
        try:
            time.sleep(2)
            CNDACCEPT(browser, "Accepted", "SEL_EVT_ACCEPTonly")
            browser.switch_to.default_content()
            browser.find_element_by_xpath(
                '//div[@class=" x-panel x-panel-noborder"]/div/div[@class="x-panel-body x-panel-body-noheader x-panel-body-noborder x-border-layout-ct"]//button[contains(text(), "Refresh")]').click()

        except NoSuchElementException:
            time.sleep(2)
            browser.switch_to.default_content()
            print "INM don't exist , Refreshing"
            browser.find_element_by_xpath(
                '//div[@class=" x-panel x-panel-noborder"]/div/div[@class="x-panel-body x-panel-body-noheader x-panel-body-noborder x-border-layout-ct"]//button[contains(text(), "Refresh")]').click()


# -----------------------------------------------------------------------------------------------

#pathing usersettings.xml
pth = path.path('usersettings.xml')
cc = csc.csclxmls.node(pth)

#check headlessmode
if cc('//item[@key="headless"]').text != 1:
    print "Not headless"
else:
    os.environ['MOZ_HEADLESS'] = '1'
    print "headless mode"

#getting path for gecko
geckopath = os.getcwd()
os.environ["PATH"] += os.pathsep + geckopath

username = cc('//item[@key="username"]').text
password = cc('//item[@key="password"]').text
start(username, password)
