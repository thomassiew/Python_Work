#! /usr/bin/env python
# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import traceback
import path
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def finditem(items=[], st=""):
    if isinstance(items, list):
        for item in items:
            if item.text.upper() == st.upper():
                element = item
                break
        else:
            element = None
    elif items:
        element = items
    else:
        element = None
    return element


def waitfor(by=By.TAG_NAME, st="body", timeout=15):
    try:
        ec = EC.presence_of_element_located((by, st))
        element = WebDriverWait(browser, timeout).until(ec)
    except:
        element = None
    return element


stm = time.time()
chs = sys.argv[1:]
StorePath = ".\\pyTemp"
StoreType = "application/octet-stream;application/zip;application/x-troff-man;application/x-zip-compressed"
website = "https://smweb.telekom.de/sm-prod/index.do?lang=zh-Hans"
ph = path.path(StorePath)
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", ph.encode())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", StoreType)
fp.update_preferences()
browser = webdriver.Firefox(firefox_profile=fp)
try:
    browser.get(website)
    li = browser.find_element_by_id("LoginUsername")
    li.click()
    li.send_keys("scheeng")
    lp = browser.find_element_by_id("LoginPassword")
    lp.click()
    lp.send_keys("Pa05w0rd")
    lb = browser.find_element_by_id("loginBtn")
    lb.click()
    cv = waitfor(By.XPATH, "//span[text()='Change Management']")
    time.sleep(5)
    cm = browser.find_elements_by_xpath("//span[@class='x-panel-header-text']")
    c = finditem(cm, "Change Management")
    c.click()
    browser.switch_to_default_content()
    cv = waitfor(By.CLASS_NAME, "x-tree-node-anchor")
    cm = browser.find_elements_by_class_name("x-tree-node-anchor")
    c = finditem(cm, "Search RfC/Change")
    c.click()
    time.sleep(2)
    for ch in chs:
        browser.switch_to_default_content()
        cv = waitfor(By.XPATH, '//iframe[@title="Display Which Changes?"]')
        cm = browser.find_element_by_xpath('//iframe[@title="Display Which Changes?"]')
        browser.switch_to.frame(cm)
        cv = waitfor(By.XPATH, '//input[@name="instance/header/number"]')
        cm = browser.find_element_by_xpath('//input[@name="instance/header/number"]')
        cm.clear()
        cm.send_keys(ch)
        browser.switch_to_default_content()
        cv = waitfor(By.XPATH, '//button[@aria-label="Start this Search (Ctrl+Shift+F6)"]')
        sb = browser.find_element_by_xpath('//button[@aria-label="Start this Search (Ctrl+Shift+F6)"]')
        c = finditem(sb, "Search")
        c.click()
        cv = waitfor(By.XPATH, '//iframe[@title="Change %s - Prompt"]' % ch)
        cm = browser.find_element_by_xpath('//iframe[@title="Change %s - Prompt"]' % ch)
        browser.switch_to.frame(cm)
        cm = browser.find_element_by_xpath('//textarea[@ref="instance/description.structure/description/description"]')
        print (cm.get_attribute('value'))
        browser.switch_to_default_content()
        cm = browser.find_element_by_xpath('//button[@aria-label="Exit Record without Saving (Alt+F3)"]')
        cm.click()
        time.sleep(2)
except:
    print (traceback.format_exc())
finally:
    time.sleep(3)
    browser.switch_to_default_content()
    cv = waitfor(By.XPATH, '//button[text()="用户信息"]')
    bt = browser.find_elements_by_xpath('//button[text()="用户信息"]')
    b = finditem(bt, "用户信息")
    b.click()
    cv = waitfor(By.XPATH, '//button[text()="注销"]')
    bt = browser.find_element_by_xpath('//button[text()="注销"]')
    b = finditem(bt, "注销")
    b.click()
    browser.find_element_by_tag_name("body").send_keys(Keys.ENTER)
browser.close()
browser.quit()
etm = time.time()
print ("%ss" % (etm - stm))
