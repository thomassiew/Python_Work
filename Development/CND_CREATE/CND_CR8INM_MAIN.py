#! /usr/bin/env python
# coding=utf-8
import filelock
import sys
import SM9_V2
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
# TODO : create cross check functions for each id so eliminate sleep time
# TODO : if fail , send email to sender or ag
# getting settings
pth = path.path('XML/settings.xml')
settings = csc.csclxmls.node(pth)

# locating directory and archives for data grabbing
directory = os.getcwd() +settings('//item[@key="createrequest"]').text
archive = os.getcwd() + settings('//item[@key="archivefolder"]').text
fail =  os.getcwd() + settings('//item[@key="failfolder"]').text

# functions
sm9 = SM9_V2.sm9_general(str(os.getpid()))
# Credentials directory.
creddir = path.path('CREDS')

global abc  # dirs
global fl  # filelock
while True:

    try:
        sm9.sm9_logging("Initiating Firefox")
        # start firefox
        sm9.sm9_firefox_start()
        # login
        sm9.sm9_logging("Starting Login Process ")
        # opening creds folder to check creds
        try:
            if os.listdir(creddir) == []:
                raise Exception("Empty dir")
            x = len(os.listdir(creddir))
            # credentials found
            for creds in os.listdir(creddir):
                modixml = os.path.basename(creds)
                a, b = modixml.split(".")
                # create lock
                fl = filelock.FileLock(creddir + "\\" + a + ".lck", .5)
                if not os.path.exists(creddir + "\\" + a + ".lck"):
                    # get cred name
                    sm9.sm9_logging("CREDS :" + a + " not lck: " + " , creating lck")
                    fl.acquire()
                    sm9.sm9_login(creds)
                    break
                else:
                    sm9.sm9_logging("Login Failed , retrying with another creds")
                    fl.release()
                x = - 1
                time.sleep(15)
                fl.release()
            if x <= 0:
                raise Exception("all locked.")
        except:
            #all credentials lock or not working.
            # creating new credential. On pause mode
            sm9.sm9_logging("No credential , creating 1")
            sm9.sm9_login_encryption()
            time.sleep(10)
            continue

        # choose nav
        sm9.sm9_logging("Open Fav and Dashboard")
        # incident management panel
        sm9.sm9_navpanel(4)
        sm9.sm9_logging("Checking folder if any ID exist")
        # -------------------------- START DATA SEARCH AND LOOPING ------------------------
        while 1:
            reload(SM9_V2)
            # check if directory contains INM folders

            if len(os.listdir(directory)) < 1:
                sm9.sm9_logging("no folders, reset")
                time.sleep(5)
            # else if INM folders exist
            else:
                no = 1
                for dirs in os.listdir(directory):
                    abc = dirs
                    fn_only = dirs.split(".")
                    sm9.sm9_logging("ID Located")
                    if os.path.isfile(directory + "\\" + dirs):
                        # check if LCK exist , if yes then next DIR
                        if os.path.exists(directory + "\\" + fn_only[0] + ".lck"):
                            sm9.sm9_logging(str(dirs) + " is locked , next inm")
                            time.sleep(15)
                        # LCK dont exist , go for the INMcreation
                        else:
                            try:
                                sm9.sm9_logging("no lck: " + dirs + " , creating new lockfile to start work")
                                open(directory + "\\" + fn_only[0] + ".lck", 'w')
                                sm9.sm9_logging("Ticket exist, commencing ticket creation .")
                                createpath = path.path(directory + "\\" + abc)
                                cr8 = csc.csclxmls.node(createpath)

                                # update ticketsent section to xml
                                cr8('//item[@key="ticketsent"]').text = str(fn_only[0])
                                createpath.write_bytes(cr8.xml)
                                # create inm starts now
                                sm9.sm9_createINM()
                                sm9.sm9_logging("Opening Ticket Creation Tab")
                                # parameters checking
                                # x16 = Title
                                cr8title = cr8('//item[@key="TITLE"]').text
                                sm9.wait_sendkeys('//*[@id="X16"]', cr8title, 20)
                                # X23 = Customer
                                cr8inm = firefoxdriver.driver.find_element_by_xpath('//*[@id="X2"]').get_attribute(
                                    'value')
                                sm9.sm9_logging("INM ID: %s" % str(cr8inm))
                                cr8custs = cr8('//item[@key="CUSTOMER"]').text
                                sm9.wait_sendkeys('//*[@id="X23"]', cr8custs, 20)
                                # X35 = category 1
                                cr8cat1 = cr8('//item[@key="CATEGORY1"]').text
                                sm9.wait_sendkeys('//*[@id="X35"]', cr8cat1, 20)
                                # X37 = category 2
                                time.sleep(3)
                                cr8cat2 = cr8('//item[@key="CATEGORY2"]').text
                                sm9.wait_sendkeys('//*[@id="X37"]', cr8cat2, 20)
                                time.sleep(3)
                                # X45 = AG
                                cr8ag = cr8('//item[@key="AG"]').text
                                sm9.wait_sendkeys('//*[@id="X45"]', cr8ag, 20)
                                # X59 = CRIC
                                cr8cric = cr8('//item[@key="CRIC"]').text
                                sm9.wait_sendkeys('//*[@id="X59"]', cr8cric, 20)
                                # X61 = Restriction
                                cr8restr = cr8('//item[@key="RESTRICTION"]').text
                                sm9.wait_sendkeys('//*[@id="X61"]', cr8restr, 20)
                                # X80 = CI
                                cr8ci = cr8('//item[@key="CI"]').text
                                sm9.wait_sendkeys('//*[@id="X80"]', cr8ci, 20)
                                # x110 = WIW
                                cr8wiw = cr8('//item[@key="WIW"]').text
                                sm9.wait_sendkeys('//*[@id="X110"]', cr8wiw, 20)
                                # x147view = Description
                                time.sleep(3)
                                cr8des = cr8('//item[@key="DESCRIPTION"]').text
                                firefoxdriver.driver.find_element_by_id('X147View').click()
                                sm9.wait_sendkeys('//*[@id="X147"]', cr8des, 20)
                                # fill in wiw
                                sm9.wait_click('//div[@id="X110Fill"]/img[@id="X110FillButton"]', 20)
                                time.sleep(5)
                                firefoxdriver.driver.switch_to.default_content()
                                print "saving now"
                                sm9.save_exit()
                                time.sleep(2)
                                sm9.save_exit()

                                for x in range(0, 9):
                                    if sm9.isElementPresent('//iframe[@title="Create New Incident"]') == True:
                                        print "Incident frame still exist.."
                                        time.sleep(1)
                                    else:
                                        break

                                if sm9.isElementPresent('//iframe[@title="Create New Incident"]') == True:
                                    sm9.sm9_logging("Ticket not created .. not moving xml away")
                                    sm9.cancel_updateinm()
                                    os.remove(directory + "\\" + fn_only[0] + ".lck")
                                    timestr1 = time.strftime("%Y%m%d-%H%M%S")
                                    cr8('//item[@key="ticketfail"]').text = timestr1

                                    createpath.write_bytes(cr8.xml)
                                    sm9.sm9_logging('moving ' + dirs + " to fail folder")
                                    sm9.sm9_logging("moving " + str(directory + "\\" + dirs) + " to " + str(
                                        fail + "\\" + str(timestr1) + "_" + dirs))
                                    os.rename(directory + "\\" + dirs,
                                              fail + "\\" + str(timestr1) + "_" + str(cr8inm) + "_" + dirs)

                                else:
                                    sm9.sm9_logging("Ticket Create.. updating xml and moving xml")
                                    timestr = time.strftime("%Y%m%d-%H%M%S")
                                    sm9.sm9_logging('moving ' + dirs + " to archive")
                                    sm9.sm9_logging("moving " + str(directory + "\\" + dirs) + " to " + str(
                                        archive + "\\" + str(timestr) + "_" + dirs))

                                    # update xml with INM

                                    cr8('//item[@key="INCIDENTID"]').text = cr8inm
                                    cr8('//item[@key="ticketcreated"]').text = "BOOM"

                                    createpath.write_bytes(cr8.xml)
                                    time.sleep(2)

                                    if not os.path.exists(archive):
                                        os.makedirs(archive)
                                    else:
                                        sm9.sm9_logging(directory + " exist")

                                    os.rename(directory + "\\" + dirs,
                                              archive + "\\" + str(timestr) + "_" + str(cr8inm) + "_" + dirs)

                                    sm9.sm9_logging('deleting lck: ' + dirs)
                                    os.remove(directory + "\\" + fn_only[0] + ".lck")

                                    sm9.sm9_logging("INM: %s created . Looking for new tickets" % cr8inm)
                            except:
                                # TODO : need to add exceptions issue if fail to create ticket
                                print traceback

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
