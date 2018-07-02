import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait


def waitpageload(idd):
    try:
        WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.ID, idd)))
        print idd + " found!"
    except TimeoutException:
        print "Loading took too much time!"


def hpesm9iframe():
    waitfor(By.XPATH, '//iframe[@title="HPE Service Manager"]')
    browser.switch_to.frame(browser.find_element_by_css_selector('iframe[title="HPE Service Manager"]'))


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


# configuring profile
StoreType = "application/octet-stream;application/zip;application/x-troff-man;application/x-zip-compressed"
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "C:\\Users\\Ysiew\\CNL\\")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", StoreType)

fp.update_preferences()
browser = webdriver.Firefox(firefox_profile=fp)

browser.get('https://smweb.telekom.de/sm-prod/index.do?lang=en')

# UserName
Username = browser.find_element_by_name('user.id')
Username.send_keys("ysiew")

# Password
PW = browser.find_element_by_id('LoginPassword')
PW.send_keys("Syc$0173556811")

# Click login button
browser.find_element_by_id('loginBtn').click()

waitpageload('ROOT/Favorites and Dashboards')
cm = browser.find_element_by_xpath("//span[text()='Favorites and Dashboards']")

cv = waitfor(By.XPATH, "//span[text()='Favorites and Dashboards']")
time.sleep(5)
cm = browser.find_elements_by_xpath("//span[@class='x-panel-header-text']")
c = finditem(cm, "Favorites and Dashboards")
c.click()

time.sleep(2)

wait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='change5to10']"))).click()
time.sleep(5)
waitfor(By.XPATH, '//iframe[@title="Change Queue: change5to10"]')
time.sleep(2)
browser.switch_to.frame(browser.find_element_by_css_selector("iframe[title='Change Queue: change5to10']"))

SM9table = browser.find_elements_by_xpath('//div/table/tbody/tr/td[2]/div')
print len(SM9table)
SM9number = len(SM9table) + 1
i = 2
while i <= SM9number:
    Chnumber = browser.find_element_by_xpath('//div[%i]/table/tbody/tr/td[2]/div' % i)
    a = Chnumber.text
    print a
    Chnumber.click()

    # HPE Service Manager iframe
    browser.switch_to.default_content()
    hpesm9iframe()

    # Change iframe
    waitfor(By.XPATH, '//iframe[@title="Change %s - Prompt"]' % a)
    browser.switch_to.frame(browser.find_element_by_css_selector('iframe[title="Change %s - Prompt"]' % a))
    time.sleep(2)

    # Type your code here
    # -----------------------------------------------------------------------------------------------------------------

    browser.find_element_by_xpath('//a[@title="Notebook tab - Specification"]').click()
    time.sleep(2)
    browser.find_element_by_xpath('//a[@title="Notebook tab - Attachments"]').click()
    time.sleep(2)
    browser.find_element_by_xpath('//a[contains(text(),"CNL")]').click()
    time.sleep(2)

    # -----------------------------------------------------------------------------------------------------------------


    browser.switch_to.default_content()
    hpesm9iframe()
    cm = browser.find_element_by_xpath('//button[@aria-label="Exit Record without Saving (Alt+F3)"]')
    cm.click()
    time.sleep(2)
    browser.switch_to.default_content()
    time.sleep(2)
    browser.switch_to.frame(browser.find_element_by_css_selector("iframe[title='Change Queue: change5to10']"))
    time.sleep(2)
    i += 1
