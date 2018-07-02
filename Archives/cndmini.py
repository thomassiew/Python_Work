import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def switch_iframe(browser, title):
    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@title="%s"]' % title)))
    time.sleep(2)
    browser.switch_to.frame(browser.find_element_by_css_selector('iframe[title="%s"]' % title))
    print "Iframe: " + title + " reached"

def check_CND_frames(browser):
    # IF CND query contains more than 1 ticket , HPE SERVICE MANAGER frame is needed .
    # This function is to particularly check if the specified frame is needed or not
    try:
        INM2 = browser.find_element_by_xpath('//div[1]/table/tbody/tr/td[2]/div')
        if INM2.is_displayed():
            browser.switch_to.default_content()
            switch_iframe(browser, "HPE Service Manager")
            print "hp frame found and entered"
    except NoSuchElementException:
        print "no hp frame needed"

def loginsm9(username, password, browser):
    # UserName
    Username = browser.find_element_by_name('user.id')
    Username.send_keys(username)
    # Password
    PW = browser.find_element_by_id('LoginPassword')
    PW.send_keys(password)
    # Click login button
    browser.find_element_by_id('loginBtn').click()


def waitpageload(idd, browser):
    try:
        loadingpage = WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.ID, idd)))
        if loadingpage.is_displayed():
            print idd + " found! , clicking....."
            time.sleep(2)
            FD = browser.find_element_by_xpath(
                "//span[contains(@class,'x-panel-header-text') and contains(text(),'Favorites and Dashboards')]")
            FD.click()
        time.sleep(2)
    except TimeoutException:
        print "Loading took too much time!"


def selectquery(type, queryname, browser):
    # Type
    # Type = 1 ( Change )
    # Type = 2 ( Incident)
    if type == 1:
        type = "Change"
    elif type == 2:
        type = "Incident"
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='%s']" % queryname))).click()
    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@title="%s Queue: %s"]' % (type, queryname))))
    time.sleep(2)
    browser.switch_to.frame(browser.find_element_by_css_selector("iframe[title='%s Queue: %s']" % (type, queryname)))


def idcrawling(browser):
    SM9table = browser.find_elements_by_xpath('//div/table/tbody/tr/td[2]/div')
    print len(SM9table)
    SM9number = len(SM9table)
    i = 1
    while i <= SM9number:
        Chnumber = browser.find_element_by_xpath('//div[%i]/table/tbody/tr/td[2]/div' % i)
        a = Chnumber.text
        print a
        i += 1


def searchchg(browser):
    FD = browser.find_element_by_xpath(
        "//span[contains(@class,'x-panel-header-text') and contains(text(),'Change Management')]")
    FD.click()
    time.sleep(2)
    CD = browser.find_element_by_id("ROOT/Change Management/Search RfC_/Change")
    CD.click()
    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@title="Display Which Changes?"]')))
    time.sleep(2)
    browser.switch_to.frame(browser.find_element_by_xpath('//iframe[@title="Display Which Changes?"]'))


def CNDACCEPT(browser, status,title):
    browser.switch_to.default_content()
    switch_iframe(browser, "Incident Queue: %s" % title)
    #Checking len of data to determine if we need HPE Service Manager Frame or not
    # if data more than one = yes  else no
    SM9table = browser.find_elements_by_xpath('//div/table/tbody/tr/td[2]/div')
    SM9number = len(SM9table)
    print "Number of data:" + str(SM9number)
    # Finding INM and click into it
    INM = browser.find_element_by_xpath('//div[1]/table/tbody/tr/td[2]/div').text
    print "INM exist , CND function commencing"
    print INM + " found!"

    WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//div[1]/table/tbody/tr/td[2]/div'))).click()

    # switching to HPE main frame?
    if SM9number > 1:
        browser.switch_to.default_content()
        switch_iframe(browser, "HPE Service Manager")
        print "HP Frame needed"
    else:
        print "HP Frame not needed"
    # switching to INM frame
    switch_iframe(browser, "Update Incident Number %s" % INM)
    print "Update incident framed found and entered"
    # locate status field
    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.ID, 'X12')))
    print "accept field located"
    Acceptfield = browser.find_element_by_id('X12')
    # change input value
    browser.execute_script("arguments[0].setAttribute('value','%s')" % (status), Acceptfield)

    #check HP Frame again
    if SM9number > 1:
        browser.switch_to.default_content()
        switch_iframe(browser, "HPE Service Manager")
        print "HP Frame needed"
    else:
        print "HP Frame not needed"
    # save and exit
    browser.find_element_by_xpath('//button[@aria-label="Save Record and Exit (Ctrl+Shift+F2)"]').click()
    # browser.find_element_by_xpath('//button[@aria-label="Exit Record without Saving (Alt+F3)"]').click()
    print "clicked save"
    time.sleep(2)
    browser.switch_to.default_content()
    switch_iframe(browser, "Incident Queue: %s" % title)
