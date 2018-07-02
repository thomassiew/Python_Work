
from selenium import webdriver

import Development.csc.csclxmls
import os
import path

# set settings
pth = path.path('settings.xml')
cc = Development.csc.csclxmls.node(pth)

# checking storetype
storetype = cc('//item[@key="storetype"]').text
# provide geckodriver path
geckopath = os.getcwd()
os.environ["PATH"] += os.pathsep + geckopath
# check if user needs additional pref or not
fp = webdriver.FirefoxProfile()
if cc('//item[@key="firefoxpref"]').text == 1:
    print "Firefox Pref : True"
    fp.set_preference("browser.download.folderList", 1)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", storetype)
    fp.update_preferences()
else:
    print "Firefox Pref : False"
    fp.update_preferences()

# setting website and access link through browser

driver = webdriver.Firefox(firefox_profile=fp)