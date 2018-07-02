import time
import path
import csc.csclxmls
import os
import EasyDialogs
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import firefoxdriver

# set settings
pth = path.path('settings.xml')
rulebase = path.path('rulebase.xml')
rules = csc.csclxmls.node(rulebase)

cc = csc.csclxmls.node(pth)
key = 'vXEXjeVp9WOAjFlRqXfJEMX3far-TuBmFquUvDoKgGw='
cipher_suite = Fernet(key)


def sm9_login_encryption():
    """
         Function ID: SM9_00
         Name : sm9_login_encryption
         Description : To encrypt username and password to creds.xml. Will check creds.xml . If available
                        will skip action
         Prerequisites : sm9 initial login page
    """
    if os.path.isfile('creds.xml'):
        print "creds.xml available , new encryption not needed."
    else:
        userpath = path.path('creds.xml')
        root = csc.csclxmls.node("<root/>")
        user = root + 'user'
        item1 = user + 'item'
        item1['key'] = "username"
        item2 = user + 'item'
        item2['key'] = "password"

        username = EasyDialogs.AskString("Username :")
        cipher_text_username = cipher_suite.encrypt(username)
        item1.text = cipher_text_username
        password = EasyDialogs.AskPassword("Password :")
        cipher_text_password = cipher_suite.encrypt(password)
        item2.text = cipher_text_password
        userpath.write_bytes(root.xml)
        print "creds.xml created"


def sm9_login():
    """
     Function ID: SM9_01
     Name : sm9_login
     Description : To login to SM9, username and password get from creds.xml
     Prerequisites : sm9 initial login page
    """
    try:
        # encryption of user and password checking
        sm9_login_encryption()
        # get username and password from xml
        creds = path.path('creds.xml')
        credslogin = csc.csclxmls.node(creds)
        # cryptography in action to decrypt
        decrypted_username = cipher_suite.decrypt(credslogin('//item[@key="username"]').text)
        decrypted_password = cipher_suite.decrypt(credslogin('//item[@key="password"]').text)
        user = decrypted_username
        passd = decrypted_password
        # UserName
        username = firefoxdriver.driver.find_element_by_name('user.id')
        username.send_keys(user)
        # Password
        pw = firefoxdriver.driver.find_element_by_id('LoginPassword')
        pw.send_keys(passd)
        # Click login button
        firefoxdriver.driver.find_element_by_id('loginBtn').click()
        print "Login button clicked , please wait...."
        loadingpage = WebDriverWait(firefoxdriver.driver, 5).until(
            ec.presence_of_element_located((By.ID, "ROOT/Favorites and Dashboards")))
        if loadingpage.is_displayed():
            print "Login Successful..."
    except IOError:
        print "Login Failed , creds.xml deleted.. please key in again"
        os.remove("creds.xml")
        sm9_login()


def sm9_navpanel(navigate):
    """
     Function ID: SM9_02
     Name : sm9_navpanel
     Description : Able to select and dropdown navigation for selection
     Parameter: navigate - Inserting integer as below will result in different navigation
                            1 = ROOT/Favorites and Dashboards
                            2 = ROOT/Change Management
                            3 = ROOT/Configuration Management
                            4 = ROOT/Incident Management
                            5 = ROOT/Problem Management
                            6 = ROOT/Service Desk
                            7 = ROOT/T-Systems Archive
     Prerequisites : sm9_login() or inside SM9 website
    """
    if navigate == 1:
        navigate = "ROOT/Favorites and Dashboards"
    elif navigate == 2:
        navigate = "ROOT/Change Management"
    elif navigate == 3:
        navigate = "ROOT/Configuration Management"
    elif navigate == 4:
        navigate = "ROOT/Incident Management"
    elif navigate == 5:
        navigate = "ROOT/Problem Management"
    elif navigate == 6:
        navigate = "ROOT/Service Desk"
    elif navigate == 7:
        navigate = "ROOT/T-Systems Archive"

    navigate2 = navigate.replace("ROOT/", "", 1)
    try:
        loadingpage = WebDriverWait(firefoxdriver.driver, 40).until(
            ec.presence_of_element_located((By.ID, navigate)))
        if loadingpage.is_displayed():
            print navigate2 + " found! , clicking....."
            time.sleep(2)
            fd = firefoxdriver.driver.find_element_by_xpath(
                "//span[contains(@class,'x-panel-header-text') and contains(text(),'%s')]" % navigate2)
            fd.click()
        time.sleep(2)
    except TimeoutException:
        print "Loading took too much time!"


def sm9_opensearch(types):
    """
    Function ID: SM9_03
    Name : sm9_opensearch
    Description : To open search display for incident , change or task
    Parameter: type - Inserting integer as below will result in different navigation
                            1 = Change
                            2 = Incident
                            3 = Task
    Prerequisites : sm9_navpanel()
    """
    searches = ""
    if types == 1:
        types = "Changes"
        print "Change chosen , opening search"
        searches = "ROOT/Change Management/Search RfC_/Change"
    elif types == 2:
        types = "Incident Records"
        print "Incident chosen , opening search"
        searches = "ROOT/Incident Management/Search Incident"
    elif types == 3:
        types = "Tasks"
        print "Task chosen , opening search"
        searches = "ROOT/Change Management/Search Tasks"

    time.sleep(1)
    cd = firefoxdriver.driver.find_element_by_id(searches)
    cd.click()
    WebDriverWait(firefoxdriver.driver, 40).until(
        ec.presence_of_element_located((By.XPATH, '//iframe[@title="Display Which %s?"]' % types)))
    time.sleep(2)
    firefoxdriver.driver.switch_to.frame(
        firefoxdriver.driver.find_element_by_xpath('//iframe[@title="Display Which %s?"]' % types))


def sm9_search_id(ids):
    """
    Function ID: SM9_04
    Name : sm9_search_id
    Description : To search ticket , incident or task
    Parameter: ID - can be Incident , Change or Task ID
    Prerequisites : sm9_opensearch()
    """
    WebDriverWait(firefoxdriver.driver, 40).until(
        ec.presence_of_element_located((By.ID, 'X13')))
    print "Search field found, proceed to pump in ID"
    searchfield = firefoxdriver.driver.find_element_by_id('X13')
    # change input value
    firefoxdriver.driver.execute_script("arguments[0].setAttribute('value','%s')" % ids, searchfield)
    search = sm9_buttons()
    search.search()
    print "ID: " + ids + " inserted , proceeding to search the following"


def sm9_favdash_query_select():
    """
         Function ID: SM9_05
         Name : sm9_favdash_query_select
         Description : To select fav and dashboard queries
         Parameter:  queryname - queryname created
         Prerequisites : sm9_navpanel()
    """
    queryname = cc('//item[@key="queryname"]').text
    WebDriverWait(firefoxdriver.driver, 15).until(
        ec.element_to_be_clickable((By.XPATH, "//span[text()='%s']" % queryname))).click()
    print "query selected and clicked"


def sm9_firefox_start():
    """
         Function ID: SM9_06
         Name : sm9_firefox_start
         Description : To start sm9 based on xml requirement
                        If headless = 1 , then firefox headless mode initiated
                        If firefoxpref =  1, then firefox prefer is needed. Preferences as below
                        Website using xml websitekeys.

    """
    # check headlessmode
    if cc('//item[@key="headless"]').text != '1':
        print "Not headless"
    elif cc('//item[@key="headless"]').text == "1":
        os.environ['MOZ_HEADLESS'] = '1'
        print "headless mode"
    weblink = cc('//item[@key="website"]').text
    firefoxdriver.driver.get(weblink)


def sm9_query_data_collection():
    """
             Function ID: SM9_07
             Name : sm9_query_data_collection
             Description : To collect data based on view type of query from fav and dashboard
             Prerequisite  :  Require the select query opened first before running
    """
    queryname = cc('//item[@key="queryname"]').text
    WebDriverWait(firefoxdriver.driver, 40).until(
        ec.presence_of_element_located((By.XPATH, '//iframe[contains(@title,"Queue: %s")]' % queryname)))
    time.sleep(2)
    firefoxdriver.driver.switch_to.frame(
        firefoxdriver.driver.find_element_by_xpath('//iframe[contains(@title,"Queue: %s")]' % queryname))
    print queryname + " iframe located and activated"

    id_list = []
    page = 1
    datacount = 0
    # file = open("testfile.txt", "w")
    directory = "C:\SM9automation\Incident\%s" % queryname
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print directory + " exist"

    while True:
        sm9table = firefoxdriver.driver.find_elements_by_xpath('//div/table/tbody/tr/td[2]/div')
        sm9number = len(sm9table)
        datacount += sm9number
        print "Page %i now" % page
        print "No of ID:" + str(datacount)
        for ID in range(1, sm9number + 1):
            idname = firefoxdriver.driver.find_element_by_xpath('//div[%i]/table/tbody/tr/td[2]/div' % ID)
            id_list.append(str(idname.text))
            idfoldername = str(idname.text)
            iddir = directory + "\\" + idfoldername
            # file.write("%s\n" % str(IDname.text))
            if not os.path.exists(iddir):
                os.makedirs(iddir)
            else:
                print idfoldername + " exist , next INM"

        try:
            nextpg = firefoxdriver.driver.find_element_by_xpath(
                '//button[@aria-label="Next Page" and @aria-disabled="false"]')
            if nextpg.is_displayed():
                nextpg.click()
                page += 1
                WebDriverWait(firefoxdriver.driver, 40).until(
                    ec.presence_of_element_located(
                        (By.XPATH, '//div/span[@class="audible-text" and contains(text(),"Current Page %i")]' % page)))
                WebDriverWait(firefoxdriver.driver, 40).until(
                    ec.presence_of_element_located((By.XPATH, '//div/table/tbody/tr/td[2]/div')))
        except NoSuchElementException:
            print " no new page , no more ticket. Data collection completed"
            print id_list
            break


def sm9_log_out():
    """
        Function ID: SM9_08
        Name : sm9_log_out
        Description : To log out
        Prerequisite  :  Require  user logged-in first
    """
    print "Logging-Out"
    time.sleep(1)
    firefoxdriver.driver.switch_to.default_content()
    userinfo = WebDriverWait(firefoxdriver.driver, 40)
    userinfo.until(ec.presence_of_element_located((By.XPATH, '//button[text()="User Information"]'))).click()
    logout = WebDriverWait(firefoxdriver.driver, 40)
    logout.until(ec.presence_of_element_located((By.XPATH, '//button[text()="Logout"]'))).click()
    popup = WebDriverWait(firefoxdriver.driver, 20)
    popup.until(ec.alert_is_present()).accept()
    print "Logged-Out"


def sm9_decline():
    # cancel fro display
    sm9btn = sm9_buttons()
    sm9btn.cancel()
    i = 1
    while i:
        inmhead = firefoxdriver.driver.find_elements_by_xpath(
            '//iframe[contains(@title,"Update Incident Number")]')
        if len(inmhead):
            print "header still exist"
            sm9btn.cancel()
            time.sleep(5)
        else:
            i = 0

    WebDriverWait(firefoxdriver.driver, 40).until(
        ec.presence_of_element_located((By.XPATH, '//iframe[contains(@title,"Display Which")]')))
    time.sleep(2)
    firefoxdriver.driver.switch_to.frame(
        firefoxdriver.driver.find_element_by_xpath('//iframe[contains(@title,"Display Which")]'))
    time.sleep(2)


def sm9_accept(ids):
    WebDriverWait(firefoxdriver.driver, 40).until(
        ec.presence_of_element_located((By.XPATH, '//iframe[contains(@title,"Update Incident Number")]')))
    time.sleep(2)
    firefoxdriver.driver.switch_to.frame(
        firefoxdriver.driver.find_element_by_xpath('//iframe[contains(@title,"Update Incident Number")]'))
    time.sleep(2)

    userinfo = WebDriverWait(firefoxdriver.driver, 20)
    userinfo.until(ec.presence_of_element_located(
        (By.XPATH, "//div/input[@id='X12']")))
    searchfield = firefoxdriver.driver.find_element_by_id('X12')
    # Change open to ACCEPT
    firefoxdriver.driver.execute_script("arguments[0].setAttribute('value','%s')" % ids, searchfield)
    # Do your work instruction
    userinfo.until(ec.presence_of_element_located(
        (By.XPATH, "//div/input[@id='X57']")))
    searchAG = firefoxdriver.driver.find_element_by_id('X57')
    assignee = firefoxdriver.driver.find_element_by_id('X63')

    ag = searchAG.get_attribute('value')
    print ag + " exist"

    k = rules('//accept/item[@AG="%s"]' % str(ag))
    abc = k['AG']
    print abc + " xml "
    if abc is not "":
        print "AG FOUND in XML: " + searchAG.get_attribute('value')
        chosen_assignee = k.text
        print "Accepted to be: " + chosen_assignee
        print chosen_assignee
        firefoxdriver.driver.execute_script("arguments[0].setAttribute('value','%s')" % chosen_assignee,
                                            assignee)

        print "trying to save now"
        firefoxdriver.driver.switch_to.default_content()
        userinfo = WebDriverWait(firefoxdriver.driver, 10)
        userinfo.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Save Record and Exit (Ctrl+Shift+F2)"]'))).click()

        time.sleep(2)

        try:
            firefoxdriver.driver.switch_to.default_content()
            Save_error = WebDriverWait(firefoxdriver.driver, 2)
            try:
                Save_error.until(
                    ec.presence_of_element_located((By.XPATH, '//p[contains(text(), "error")]')))
                message = " hidden message occur , cancelling"
            except:
                Save_error.until(
                    ec.presence_of_element_located(
                        (By.XPATH, '//button[contains(text(), "OK")]'))).send_keys(Keys.ENTER)
                message = " messagebox of error pop up , cancelling"
            print message
            sm9_cancel()
        except:
            print "nothing happen, saving is secured"

            inmhead = firefoxdriver.driver.find_elements_by_xpath(
                '//iframe[contains(@title,"Update Incident Number")]')
            if len(inmhead):
                print "header still exist"
                userinfo = WebDriverWait(firefoxdriver.driver, 10)
                userinfo.until(ec.presence_of_element_located(
                    (By.XPATH, '//button[@aria-label="Exit Record without Saving (Alt+F3)"]'))).click()
            else:
                i = 0
            WebDriverWait(firefoxdriver.driver, 40).until(
                ec.presence_of_element_located((By.XPATH, '//iframe[contains(@title,"Display Which")]')))
            time.sleep(2)
            firefoxdriver.driver.switch_to.frame(
                firefoxdriver.driver.find_element_by_xpath('//iframe[contains(@title,"Display Which")]'))
            time.sleep(2)


class sm9_buttons():
    def __init__(self):
        firefoxdriver.driver.switch_to.default_content()
        sm9driver = WebDriverWait(firefoxdriver.driver, 10)
        self.driver = sm9driver

    def cancel(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[contains(@aria-label, "(Alt+F3")]'))).click()

    def search(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Start this Search (Ctrl+Shift+F6)"]'))).click()

    def save_exit(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Save Record and Exit (Ctrl+Shift+F2)"]'))).click()

    def save_only(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Save Record (Ctrl+Shift+F4)"]'))).click()

    def refresh(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH,
             '//div[@class=" x-panel x-panel-noborder"]/div/div[@class="x-panel-body x-panel-body-noheader x-panel-body-noborder x-border-layout-ct"]//button[contains(text(),"Refresh")]'))).click()
