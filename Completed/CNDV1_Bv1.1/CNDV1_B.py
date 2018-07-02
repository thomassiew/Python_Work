#! /usr/bin/env python
# coding=utf-8

import sys

reload(sys)
import SM9_V2
import csc.csclxmls, path, traceback, time, firefoxdriver, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Getting XML from XML folders
# 3 rules , accept , dispatch and email
ruleaccpt = path.path('XML/Rule_Accept.xml')
rulewi = path.path('XML/Rule_Dispatch.xml')
ruleemail = path.path('XML/Rule_Email.xml')
# SM9 wait function
waiting = SM9_V2.sm9_wait()
# getting node from all 3 XMLs
R_accpt = csc.csclxmls.node(ruleaccpt)
R_disp = csc.csclxmls.node(rulewi)
R_email = csc.csclxmls.node(ruleemail)

# getting settings
pth = path.path('XML/settings.xml')
settings = csc.csclxmls.node(pth)

# locating directory and archives for data grabbing
directory = settings('//item[@key="ticketfolder"]').text
archive = settings('//item[@key="archivefolder"]').text

#buttons

buttons = SM9_V2.sm9_buttons()

global abc

# -------------------------- CSC TEMPLATE ------------------------
# cfg = csc.csclxmls.node.cfgfile()
while True:
    # if cfg('/root/item[@key="Pid check"]').text:
    #     if not cfg.pidfilecheck():
    #         print cfg('/root/item[@key="Exit Error"]').text
    #         sys.exit(1)
    try:
        # -------------------------- CSC TEMPLATE ------------------------

        SM9_V2.sm9_logging("Initiating Firefox")
        # start firefox
        SM9_V2.sm9_firefox_start()
        # login
        SM9_V2.sm9_logging("Starting Login Process ")
        SM9_V2.sm9_login()
        # choose nav
        SM9_V2.sm9_logging("Open Fav and Dashboard")
        SM9_V2.sm9_navpanel(4)
        # Open search
        SM9_V2.sm9_opensearch(2)
        SM9_V2.sm9_logging("Search Opened")

        SM9_V2.sm9_logging("Checking folder if any ID exist")
        # -------------------------- START DATA SEARCH AND LOOPING ------------------------
        while 1:
            reload(SM9_V2)
            # check if directory contains INM folders
            #if not (path.path(directory).dirs and path.path(directory).files):
            # if os.listdir(directory) == []:
            if len(os.listdir(directory)) < 1:
                SM9_V2.sm9_logging("no folders, reset")
                time.sleep(5)
            # else if INM folders exist
            else:
                no = 1
                for dirs in os.listdir(directory):
                    abc = dirs

                    SM9_V2.sm9_logging("ID Located")
                    if os.path.isdir(directory + "\\" + dirs):
                        # check if LCK exist , if yes then next DIR
                        if os.path.exists(directory + "\\" + dirs + ".lck"):
                            SM9_V2.sm9_logging(str(dirs) + " is locked , next inm")
                        # LCK dont exist , go for the INM
                        else:
                            SM9_V2.sm9_logging("no lck: " + dirs + " , creating new lockfile to start work")
                            open(directory + "\\" + dirs + ".lck", 'w')
                            SM9_V2.sm9_search_id(dirs)
                            # -------------------------- INM ACCEPTANCE WORK COMMENCE ------------------------
                            # jumping from Display Which frame to Update Incident Number frame
                            waiting.wait_switchframe('//iframe[contains(@title,"Update Incident Number")]', 20)
                            # time.sleep(2)
                            # located X12 which is the status input cell
                            try:
                                WebDriverWait(firefoxdriver.driver, 10).until(ec.presence_of_element_located(
                                    (By.XPATH, "//div/input[@id='X12']")))
                                SM9_V2.sm9_logging("X12 found , resuming work")
                                searchfield = firefoxdriver.driver.find_element_by_id('X12')
                                # Change status open to accept
                                firefoxdriver.driver.execute_script("arguments[0].setAttribute('value','Accepted')",
                                                                    searchfield)
                                # Collect elements for later usage

                                # X24 = Title Description
                                # X33 = Customer
                                # X57 = Assignment GROUP
                                # X63 = Assignee
                                # X76 = Priority number
                                waiting.wait_only("//div/input[@id='X57']", 10)
                                description = firefoxdriver.driver.find_element_by_id('X24')
                                customer = firefoxdriver.driver.find_element_by_id("X33")
                                searchAG = firefoxdriver.driver.find_element_by_id('X57')
                                assignee = firefoxdriver.driver.find_element_by_id('X63')
                                prio = firefoxdriver.driver.find_element_by_id("X76")
                                # once found ID , get it's value
                                ag = searchAG.get_attribute('value')
                                title = description.get_attribute('value')
                                cust = customer.get_attribute('value')
                                pr = prio.get_attribute('value')
                                SM9_V2.sm9_logging(ag + " exist")
                                # -------------------------- INM ACCEPTANCE STAGE 1 : ACCEPT! START------------------------
                                # Checking if assigning is needed by replacing X57 AG into xml.
                                # Wouldn't have error as it's controlled through queries
                                # and controlled environment syncing between XML and SM9 queries ag
                                Assign = R_accpt('//accept/item[@key="%s"]' % str(ag)).text
                                firefoxdriver.driver.execute_script("arguments[0].setAttribute('value','%s')" % Assign,
                                                                    assignee)
                                # -------------------------- INM ACCEPTANCE STAGE 2 : DISPATCH! START------------------------
                                # Looking for AG requirement to dispatch to other AG through WI ,
                                # done by replacing X57 AG into XML , if exist go ahead to check if not then continue
                                WI_AG = R_disp('//item[@key="%s"]/..' % ag)
                                if WI_AG is not None:
                                    move_ag = True
                                    cond_task = WI_AG.conditions.item.text
                                    for x in cond_task:
                                        # check through all WI if it matches
                                        if x.lower() in title.lower():
                                            SM9_V2.sm9_logging("WI: " + x + " exist, remain in queue")
                                            # if matches , AG dispatch is false.
                                            move_ag = False
                                            break
                                    # if no WI matches to title , AG move is True
                                    # will change to AG value based on XML Dispatch Rules
                                    if move_ag == True:
                                        SM9_V2.sm9_logging(" no identical , moving to new ag ")
                                        new_ag = R_disp('//item[@key="%s"]' % ag).text
                                        SM9_V2.sm9_logging('new ag = ' + new_ag)
                                        firefoxdriver.driver.execute_script(
                                            "arguments[0].setAttribute('value','%s')" % new_ag,
                                            searchAG)
                                        # -------------------------- INM ACCEPTANCE STAGE 3 : EMAIL! START------------------------
                                else:
                                    # mailfolder is where we will place the xml
                                    # place the AG into WI_EMAIl to see if it fits
                                    mailfolder = settings('//item[@key="emailfolder"]').text
                                    WI_EMAIL = R_email('//item[@key="%s"]' % ag)
                                    # IF WI_EMAIL is none and exist then do following below
                                    if WI_EMAIL is not None:
                                        # mail_xml is the xml name with INM rule for emailing that we will send to EMAIL PC
                                        mail_xml = path.path(mailfolder + "\%s.xml" % dirs)
                                        inm_xml = csc.csclxmls.node('<root/>')
                                        # splitting to and cc
                                        emailing = WI_EMAIL.text.split('/')
                                        # getting elements for emailing
                                        TO = emailing[0]
                                        CC = emailing[1]
                                        BCC = WI_EMAIL._parent.emailitem('//item[@key="BCC"]').text
                                        Subject = WI_EMAIL._parent.emailitem('//item[@key="Subject"]').text % (
                                            cust, pr, dirs, title)
                                        Body = WI_EMAIL._parent.emailitem('//item[@key="Body"]').text % ag
                                        # creating XML to another PC
                                        e_head = inm_xml + 'email'
                                        item1 = e_head + 'item'
                                        item1['key'] = "TO"
                                        item1.text = TO
                                        item2 = e_head + 'item'
                                        item2['key'] = "CC"
                                        item2.text = CC
                                        item3 = e_head + 'item'
                                        item3['key'] = "BCC"
                                        item3.text = BCC
                                        item4 = e_head + 'item'
                                        item4['key'] = "Subject"
                                        item4.text = Subject
                                        item5 = e_head + 'item'
                                        item5['key'] = "Body"
                                        item5.text = Body

                                        inm_xml.write(mail_xml)
                                # -------------------------- INM ACCEPTANCE STAGE END ----------------------------
                                SM9_V2.sm9_logging("trying to save now")
                                firefoxdriver.driver.switch_to.default_content()
                                buttons = SM9_V2.sm9_buttons()
                                buttons.save_exit()
                                time.sleep(3)
                            except:
                                firefoxdriver.driver.switch_to.default_content()
                                SM9_V2.sm9_logging("X12 not found. moving on")
                                buttons.cancel_updateinm()
                                time.sleep(3)
                            finally:
                                # error handler for SM9 to ensure it doesnt get stucked on the INM page
                                try:
                                    firefoxdriver.driver.switch_to.default_content()

                                    try:
                                        waiting.wait_only('//p[contains(text(), "error")]', 2)
                                    except:
                                        waiting.wait_sendenter('//button[contains(text(), "OK")]', 2)
                                    buttons.cancel_updateinm()
                                except:
                                    SM9_V2.sm9_logging("no error, saving is secured")
                                    inmhead = firefoxdriver.driver.find_elements_by_xpath(
                                        '//iframe[contains(@title,"Update Incident Number")]')
                                    if len(inmhead):
                                        print "header still exist"
                                        firefoxdriver.driver.switch_to.default_content()
                                        buttons.cancel_updateinm()
                                    else:
                                        i = 0
                                finally:
                                    waiting.wait_switchframe('//iframe[contains(@title,"Display Which")]', 40)
                                    # time.sleep(2)
                                SM9_V2.sm9_logging('Accepted')

                                # works end here ---------------------------------------------------
                                timestr = time.strftime("%Y%m%d-%H%M%S")

                                SM9_V2.sm9_logging('moving ' + dirs + " to archive")
                                SM9_V2.sm9_logging("moving " + str(directory + "\\" + dirs) + " to " + str(
                                    archive + "\\" + dirs + str(timestr)))
                                if not os.path.exists(archive):
                                    os.makedirs(archive)
                                else:
                                    SM9_V2.sm9_logging(directory + " exist")
                                os.rename(directory + "\\" + dirs, archive + "\\" + dirs + "_" + str(timestr))

                                SM9_V2.sm9_logging('deleting lck: ' + dirs)
                                os.remove(directory + "\\" + dirs + ".lck")
                        SM9_V2.sm9_logging(str(no))
                        no += 1
                        SM9_V2.sm9_logging("going back to check folder")
                        time.sleep(5)
    except:
        SM9_V2.sm9_logging(traceback.format_exc())
        if os.path.exists(directory + "\\" + abc  + ".lck"):
            os.remove(directory + "\\" + abc + ".lck")
        SM9_V2.sm9_logging(abc + ".lck deleted due to exception." )
    finally:
        try:
            firefoxdriver.driver.switch_to.default_content()
            SM9_V2.sm9_log_out()
        except:
            SM9_V2.sm9_logging("Cant logout, proceeding to close and restart")
        finally:
            waiting.wait_click('//a[@id="loginAgain"]', 20)
            #firefoxdriver.driver.quit()
            SM9_V2.sm9_logging("Quitting Firefox , removing geckodriver and attempt restart in 300 secs")
            time.sleep(300)

            # if cfg('/root/item[@key="Pid check"]').text:
            #     if cfg.pidfilecheck():
            #         print cfg('/root/item[@key="Exit"]').text
            #         cfg.pidfile.unlink()
                   # sys.exit()
