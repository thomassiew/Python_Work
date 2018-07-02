import time
import path
import glob
import csc.csclxmls
import os
import getpass
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import firefoxdriver

# set settings
pth = path.path('XML/settings.xml')

cc = csc.csclxmls.node(pth)
key = 'vXEXjeVp9WOAjFlRqXfJEMX3far-TuBmFquUvDoKgGw='
cipher_suite = Fernet(key)


class sm9_general():
    def __init__(self, namefile):
        self.name = namefile
        firefoxdriver.driver.switch_to.default_content()
        sm9driver = WebDriverWait(firefoxdriver.driver, 10)
        self.driver = sm9driver

    def sm9_login_encryption(self):
        """
             Function ID: SM9_00
             Name : sm9_login_encryption
             Description : To encrypt username and password to creds.xml. Will check creds.xml . If available
                            will skip action
             Prerequisites : sm9 initial login page
        """
        if os.path.isfile('CREDS/' + self.name + '.xml'):
            self.sm9_logging("creds.xml available , new encryption not needed.")
        else:
            self.sm9_logging("no creds , please key in your credentials")
            userpath = path.path('CREDS/' + self.name + '.xml')
            root = csc.csclxmls.node("<root/>")
            user = root + 'user'
            item1 = user + 'item'
            item1['key'] = "username"
            item2 = user + 'item'
            item2['key'] = "password"

            username = raw_input("Username :")
            cipher_text_username = cipher_suite.encrypt(username)
            item1.text = cipher_text_username
            password = getpass.getpass('Password:')
            cipher_text_password = cipher_suite.encrypt(password)
            item2.text = cipher_text_password
            userpath.write_bytes(root.xml)
            self.sm9_logging("credential: " + self.name + ".xml created")
    def sm9_login(self,a):
        """
         Function ID: SM9_01
         Name : sm9_login
         Description : To login to SM9, username and password get from creds.xml
         Prerequisites : sm9 initial login page
        """
        creds = path.path('CREDS/' + a)
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
        self.sm9_logging("Login button clicked , please wait....")
        loadingpage = WebDriverWait(firefoxdriver.driver, 15).until(
            ec.presence_of_element_located((By.ID, "ROOT/Favorites and Dashboards")))
        if loadingpage.is_displayed():
            self.sm9_logging("Login Successful...")


    def sm9_navpanel(self, navigate):
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
                self.sm9_logging(navigate2 + " found! , clicking.....")
                time.sleep(2)
                fd = firefoxdriver.driver.find_element_by_xpath(
                    "//span[contains(@class,'x-panel-header-text') and contains(text(),'%s')]" % navigate2)
                fd.click()
            time.sleep(2)
        except TimeoutException:
            self.sm9_logging("Loading took too much time!")

    def sm9_opensearch(self, types):
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
            self.sm9_logging("Change chosen , opening search")
            searches = "ROOT/Change Management/Search RfC_/Change"
        elif types == 2:
            types = "Incident Records"
            self.sm9_logging("Incident chosen , opening search")
            searches = "ROOT/Incident Management/Search Incident"
        elif types == 3:
            types = "Tasks"
            self.sm9_logging("Task chosen , opening search")
            searches = "ROOT/Change Management/Search Tasks"

        time.sleep(1)

        cd = firefoxdriver.driver.find_element_by_id(searches)
        cd.click()

        self.wait_switchframe('//iframe[@title="Display Which %s?"]' % types, 40)

    def sm9_search_id(self, ids):
        """
        Function ID: SM9_04
        Name : sm9_search_id
        Description : To search ticket , incident or task
        Parameter: ID - can be Incident , Change or Task ID
        Prerequisites : sm9_opensearch()
        """
        WebDriverWait(firefoxdriver.driver, 40).until(
            ec.presence_of_element_located((By.ID, 'X13')))
        self.sm9_logging("Search field found, proceed to pump in ID")
        searchfield = firefoxdriver.driver.find_element_by_id('X13')
        # change input value
        firefoxdriver.driver.execute_script("arguments[0].setAttribute('value','%s')" % ids, searchfield)

        self.search()
        self.sm9_logging("ID: " + ids + " inserted , proceeding to search the following")

    def sm9_favdash_query_select(self):
        """
             Function ID: SM9_05
             Name : sm9_favdash_query_select
             Description : To select fav and dashboard queries
             Parameter:  queryname - queryname created
             Prerequisites : sm9_navpanel()
        """
        queryname = cc('//item[@key="queryname"]').text

        self.wait_click("//span[text()='%s']" % queryname, 15)
        self.sm9_logging("query selected and clicked")

    def sm9_firefox_start(self):
        """
             Function ID: SM9_06
             Name : sm9_firefox_start
             Description : Get Website based on weblink
        """
        weblink = cc('//item[@key="website"]').text
        firefoxdriver.driver.get(weblink)

    def sm9_query_data_collection(self):
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
        self.sm9_logging(queryname + " iframe located and activated")
        id_list = []
        page = 1
        datacount = 0
        # file = open("testfile.txt", "w")
        directory = cc('//item[@key="ticketfolder"]').text
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            self.sm9_logging(directory + " exist")
        while True:
            sm9table = firefoxdriver.driver.find_elements_by_xpath('//div/table/tbody/tr/td[2]/div')
            sm9number = len(sm9table)
            datacount += sm9number
            self.sm9_logging("Page %i now" % page)
            self.sm9_logging("No of ID:" + str(datacount))
            for ID in range(1, sm9number + 1):
                idname = firefoxdriver.driver.find_element_by_xpath('//div[%i]/table/tbody/tr/td[2]/div' % ID)
                id_list.append(str(idname.text))
                idfoldername = str(idname.text)
                iddir = directory + "\\" + idfoldername
                # file.write("%s\n" % str(IDname.text))
                if not os.path.exists(iddir):
                    os.makedirs(iddir)
                else:
                    self.sm9_logging(idfoldername + " exist , next INM")
            try:
                nextpg = firefoxdriver.driver.find_element_by_xpath(
                    '//button[@aria-label="Next Page" and @aria-disabled="false"]')
                if nextpg.is_displayed():
                    nextpg.click()
                    page += 1

                    self.wait_only('//div/span[@class="audible-text" and contains(text(),"Current Page %i")]', 40)
                    self.wait_only('//div/table/tbody/tr/td[2]/div', 40)

            except NoSuchElementException:
                self.sm9_logging(" no new page , no more ticket. Data collection completed")
                print id_list
                break

    def sm9_log_out(self):
        """
            Function ID: SM9_08
            Name : sm9_log_out
            Description : To log out
            Prerequisite  :  Require  user logged-in first
        """
        self.sm9_logging("Logging-Out")
        time.sleep(1)
        firefoxdriver.driver.switch_to.default_content()
        userinfo = WebDriverWait(firefoxdriver.driver, 40)
        userinfo.until(ec.presence_of_element_located((By.XPATH, '//button[text()="User Information"]'))).click()
        logout = WebDriverWait(firefoxdriver.driver, 40)
        logout.until(ec.presence_of_element_located((By.XPATH, '//button[text()="Logout"]'))).click()
        popup = WebDriverWait(firefoxdriver.driver, 20)
        popup.until(ec.alert_is_present()).accept()
        self.sm9_logging("Logged-Out")

    def sm9_logging(self, message):
        printtime = time.strftime("%Y%m%d_%H%M%S")
        a = "[" + printtime + "] " + "[ PID: " + self.name + "] " + message + "\n"
        print a
        timeslot = time.strftime("%Y%m%d")
        log = "CND_WORKER_ACCEPT_%s.log" % timeslot
        logfile = open(os.getcwd() + "/LOGS/" + log, "a+")
        logfile.write(a)
        logfile.close()

    def cancel_displaywhich(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Cancel (Alt+F3)"]'))).click()
        self.sm9_logging("Button Cancelled Clicked")

    def cancel_updateinm(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Exit Record without Saving (Alt+F3)"]'))).click()
        self.sm9_logging("Button Cancelled Clicked")

    def search(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Start this Search (Ctrl+Shift+F6)"]'))).click()
        self.sm9_logging("Button Searched Clicked")

    def save_exit(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Save Record and Exit (Ctrl+Shift+F2)"]'))).click()
        self.sm9_logging("Button Save & Exit Clicked")

    def save_only(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH, '//button[@aria-label="Save Record (Ctrl+Shift+F4)"]'))).click()
        self.sm9_logging("Button Save Clicked")

    def refresh(self):
        self.driver.until(ec.presence_of_element_located(
            (By.XPATH,
             '//div[@class=" x-panel x-panel-noborder"]/div/div[@class="x-panel-body x-panel-body-noheader x-panel-body-noborder x-border-layout-ct"]//button[contains(text(),"Refresh")]'))).click()
        self.sm9_logging("Button Refresh clicked")

    def wait_only(self, xpaths, seconds):
        try:
            WebDriverWait(firefoxdriver.driver, seconds).until(ec.presence_of_element_located(
                (By.XPATH, xpaths)))
            self.sm9_logging(xpaths + " found")
        except:
            self.sm9_logging(xpaths + " cant be found")

    def wait_click(self, xpaths, seconds):
        try:
            WebDriverWait(firefoxdriver.driver, seconds).until(ec.presence_of_element_located(
                (By.XPATH, xpaths))).click()
            self.sm9_logging(xpaths + " found and clicked")
        except:
            self.sm9_logging(xpaths + " cant be found")

    def wait_switchframe(self, xpaths, seconds):
        try:
            WebDriverWait(firefoxdriver.driver, seconds).until(ec.presence_of_element_located(
                (By.XPATH, xpaths)))
            time.sleep(2)
            firefoxdriver.driver.switch_to.frame(
                firefoxdriver.driver.find_element_by_xpath(xpaths))
            self.sm9_logging(xpaths + " found and switched to")
        except:
            self.sm9_logging(xpaths + " cant be found")

    def wait_sendenter(self, xpaths, seconds):
        try:
            WebDriverWait(firefoxdriver.driver, seconds).until(ec.presence_of_element_located(
                (By.XPATH, xpaths)))
            time.sleep(2)
            firefoxdriver.driver.switch_to.frame(
                firefoxdriver.driver.find_element_by_xpath(xpaths)).send_keys(Keys.ENTER)
            self.sm9_logging(xpaths + " found and entered")
        except:
            self.sm9_logging(xpaths + " cant be found")
