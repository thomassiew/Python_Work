import path, csc.csclxmls, os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as Options


# set settings
pth = path.path('XML/settings.xml')
cc = csc.csclxmls.node(pth)

# checking storetype
storetype = cc('//item[@key="storetype"]').text
# provide geckodriver path
geckopath = os.getcwd()
os.environ["PATH"] += os.pathsep + geckopath
# check if user needs additional pref or not
# headless or not
opt = Options()
if cc('//item[@key="headless"]').text != '1':
    print "Not headless"
elif cc('//item[@key="headless"]').text == '1':
    opt.add_argument('-headless')
    print "headless"

fp = webdriver.FirefoxProfile()
if cc('//item[@key="firefoxpref"]').text == "1":
    print "Firefox Pref : True"
    fp.set_preference("browser.download.folderList", 1)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", storetype)
    fp.update_preferences()
else:
    print "Firefox Pref : False"
    fp.update_preferences()

# setting website and access link through browser

driver = webdriver.Firefox(firefox_profile=fp, firefox_options=opt)
