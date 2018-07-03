#! /usr/bin/env python
# coding=utf-8
import filelock
import sys
import SM9_V2
import string
import csc.csclxmls
import path
import traceback
import time
import firefoxdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

reload(sys)

# getting settings
pth = path.path('XML/settings.xml')
settings = csc.csclxmls.node(pth)

# locating directory and archives for data grabbing
directory = settings('//item[@key="ticketfolder"]').text
xmlfolder = settings('//item[@key="dataxml"]').text

# functions

sm9 = SM9_V2.sm9_general(str(os.getpid()))
creddir = path.path('CREDS')

global abc
global fl
while True:

    try:

        sm9.sm9_logging("Initiating Firefox")
        # start firefox
        sm9.sm9_firefox_start()
        # login
        sm9.sm9_logging("Starting Login Process ")
        # opening folder to check creds
        i = 1
        while i:
            try:
                # TODO : FIX THE FOR FAIL THEN CREATE WIW
                if len(os.listdir(creddir)) < 1:
                    sm9.sm9_logging("No creds in folder")
                    raise ValueError("No creds in folder")
                else:
                    for creds in os.listdir(creddir):

                        modixml = os.path.basename(creds)
                        a, b = modixml.split(".")
                        fl = filelock.FileLock(creddir + "\\" + a + ".lck", .5)
                        if not os.path.exists(creddir + "\\" + a + ".lck"):

                            # get cred name
                            sm9.sm9_logging("CREDS :" + a + " not lck: " + " , creating lck")
                            fl.acquire(timeout=3)
                            try:
                                sm9.sm9_login(creds)
                                i = 0
                            except:
                                sm9.sm9_logging("Login Failed , retrying with another creds")
                        else:
                            raise ValueError("all lcked")

            except:
                sm9.sm9_logging("All creds are used , Please create a new one")
                sm9.sm9_login_encryption()
                time.sleep(50)

        # choose nav

        sm9.sm9_logging("Open Fav and Dashboard")
        sm9.sm9_navpanel(4)
        # Open search
        sm9.sm9_opensearch(2)
        sm9.sm9_logging("Search Opened")

        sm9.sm9_logging("Checking folder if any ID exist")
        # -------------------------- START DATA SEARCH AND LOOPING ------------------------
        while 1:
            reload(SM9_V2)
            # check if directory contains INM folders
            # if not (path.path(directory).dirs and path.path(directory).files):
            # if os.listdir(directory) == []:
            if len(os.listdir(directory)) < 1:
                sm9.sm9_logging("no folders, reset")
                time.sleep(5)
            # else if INM folders exist
            else:
                no = 1
                for dirs in os.listdir(directory):
                    abc = dirs

                    sm9.sm9_logging("ID Located")
                    if os.path.isdir(directory + "\\" + dirs):
                        # check if LCK exist , if yes then next DIR
                        if os.path.exists(directory + "\\" + dirs + ".lck"):
                            sm9.sm9_logging(str(dirs) + " is locked , next inm")
                        # LCK dont exist , go for the INM
                        else:
                            sm9.sm9_logging("no lck: " + dirs + " , creating new lockfile to start work")
                            open(directory + "\\" + dirs + ".lck", 'w')
                            sm9.sm9_search_id(dirs)
                            # -------------------------- INM ACCEPTANCE WORK COMMENCE ------------------------
                            # jumping from Display Which frame to Update Incident Number frame
                            sm9.wait_switchframe('//iframe[contains(@title,"%s")]' % dirs, 20)
                            # time.sleep(2)
                            # located X12 which is the status input cell
                            # firefoxdriver.driver.switch_to.frame(
                            #     firefoxdriver.driver.find_element_by_xpath('//iframe[contains(@title,"Update Incident Number")]'))
                            try:
                                WebDriverWait(firefoxdriver.driver, 10).until(ec.presence_of_element_located(
                                    (By.XPATH, "//div/input[@id='X12']")))
                                sm9.sm9_logging("X12 status id found , resuming work")

                                # Collect elements for later usage

                                # X24 = Title Description
                                # X33 = Customer
                                # X57 = Assignment GROUP
                                # X63 = Assignee
                                # X76 = Priority number

                                Tdescription = sm9.wait_getdata(
                                    '//input[contains(@name,"instance/brief.description")]',10)
                                customer = sm9.wait_getdata(
                                    '//input[contains(@alias,"instance/tsi.mandant.name")]', 10)
                                searchAG = sm9.wait_getdata(
                                    '//input[contains(@name,"instance/assignment")]', 10)
                                assignee = sm9.wait_getdata(
                                    '//input[contains(@name,"instance/assignee.name")]', 10)
                                prio = sm9.wait_getdata(
                                    '//input[contains(@name,"instance/priority.code")]', 10)
                                # once found ID , get it's value
                                title = Tdescription.get_attribute('value')
                                ag = searchAG.get_attribute('value')
                                cust = customer.get_attribute('value')
                                pr = prio.get_attribute('value')
                                print title
                                print ag
                                print cust
                                print pr



                                # CREATING XML BASED ON FIELDS FOUND -------------------------------
                                datafolder = settings('//item[@key="dataxml"]').text
                                print "1"
                                # TODO XML CREATOR

                                data_xml = path.path(xmlfolder + '/%s.xml' % dirs)
                                inm_xml = csc.csclxmls.node('<root/>')
                                print "2"
                                # X24 = Title Description
                                # X33 = Customer
                                # X57 = Assignment GROUP
                                # X63 = Assignee
                                # X76 = Priority number
                                # creating XML to another PC
                                e_head = inm_xml + 'data'
                                item1 = e_head + 'item'
                                item1['key'] = "TITLE"
                                item1.text = title
                                item2 = e_head + 'item'
                                item2['key'] = "CUSTOMER"
                                item2.text = cust
                                item3 = e_head + 'item'
                                item3['key'] = "PRIORITY"
                                item3.text = pr
                                item4 = e_head + 'item'
                                item4['key'] = "ASSIGNMENT GROUP"
                                item4.text = ag

                                inm_xml.write(data_xml)
                                print "3"
                                sm9.cancel_updateinm()
                                # TODO : CANCELLING
                                time.sleep(3)
                            except:
                                firefoxdriver.driver.switch_to.default_content()
                                sm9.sm9_logging("X12 not found. moving on")
                                sm9.cancel_updateinm()
                                time.sleep(3)
                            finally:
                                # error handler for SM9 to ensure it doesnt get stucked on the INM page
                                try:
                                    firefoxdriver.driver.switch_to.default_content()

                                    try:
                                        sm9.wait_only('//p[contains(text(), "error")]', 2)
                                    except:
                                        sm9.wait_sendenter('//button[contains(text(), "OK")]', 2)
                                    sm9.cancel_updateinm()
                                except:
                                    sm9.sm9_logging("no error, saving is secured")
                                    inmhead = firefoxdriver.driver.find_elements_by_xpath(
                                        '//iframe[contains(@title,"Update Incident Number")]')
                                    if len(inmhead):
                                        print "header still exist"
                                        firefoxdriver.driver.switch_to.default_content()
                                        sm9.cancel_updateinm()
                                    else:
                                        i = 0
                                finally:
                                    sm9.wait_switchframe('//iframe[contains(@title,"Display Which")]', 40)
                                    # time.sleep(2)
                                sm9.sm9_logging('Accepted')

                                # works end here ---------------------------------------------------


                                sm9.sm9_logging('deleting lck: ' + dirs)
                                os.remove(directory + "\\" + dirs + ".lck")
                        sm9.sm9_logging(str(no))
                        no += 1
                        sm9.sm9_logging("going back to check folder")
                        time.sleep(5)
    except:
        sm9.sm9_logging(traceback.format_exc())
        if os.path.exists(directory + "\\" + abc + ".lck"):
            os.remove(directory + "\\" + abc + ".lck")
        sm9.sm9_logging(abc + ".lck deleted due to exception.")
        fl.release()
    finally:
        try:
            firefoxdriver.driver.switch_to.default_content()
            sm9.sm9_log_out()
        except:
            sm9.sm9_logging("Cant logout, proceeding to close and restart")
        finally:
            sm9.wait_click('//a[@id="loginAgain"]', 20)

            sm9.sm9_logging("Quitting Firefox , removing geckodriver and attempt restart in 300 secs")
            time.sleep(300)
