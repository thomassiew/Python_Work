#! /usr/bin/env python
# coding=utf-8
import win32com.client as win32

import csc.csclxmls, path, traceback, time, os,sys

def mail_logging(message):
    printtime = time.strftime("%Y%m%d_%H%M%S")
    a = "[" + printtime + "] " + message + "\n"
    print a
    timeslot = time.strftime("%Y%m%d")
    log = "CND_%s.log" % timeslot
    logfile = open(os.getcwd() + "/LOGS/" + log, "a+")
    logfile.write(a)
    logfile.close()

timestr = time.strftime("%Y%m%d-%H%M%S")
# getting settings
pth = path.path('XML/settings.xml')
settings = csc.csclxmls.node(pth)

# directory placing for Mail and Mail Archive
maildirectory = settings('//item[@key="emailfolder"]').text
mailarchive = maildirectory  + "\..\ArchiveEmailing"
cfg = csc.csclxmls.node.cfgfile()

# ------------------------- CSC Template --------------------
if cfg('/root/item[@key="Pid check"]').text:
    if not cfg.pidfilecheck():
        print cfg('/root/item[@key="Exit Error"]').text
        sys.exit(1)
    try:
# ------------------------- CSC Template --------------------
    # create mail and mailarchive directory if dont exist
        if not os.path.exists(maildirectory):
            os.makedirs(maildirectory)
        if not os.path.exists(mailarchive):
            os.makedirs(mailarchive)
    # starting point of infinite loop
        while 1:
            # check if directory contains INM folders
            if len(os.listdir(maildirectory)) < 1:
                mail_logging("no folders, reset")
                time.sleep(5)
            # else if INM folders exist
            else:
                for dirs in os.listdir(maildirectory):
                    print dirs
                    mail_logging("mail xml exists")
                    xmlpth = path.path(maildirectory + "\\" + dirs)
                    xmlmail = csc.csclxmls.node(xmlpth)
                    TO = xmlmail('//item[@key="TO"]').text
                    CC = xmlmail('//item[@key="CC"]').text
                    BCC =  xmlmail('//item[@key="BCC"]').text
                    Subject = xmlmail('//item[@key="Subject"]').text
                    maila = xmlmail('//item[@key="Body"]').text
                    Mailb = maila.replace("{","<")
                    Body = Mailb.replace("}",">")

                    # outlook create item
                    outlook = win32.Dispatch('outlook.application')
                    mail = outlook.CreateItem(0)
                    mail.To = TO
                    mail.Cc = CC
                    mail.Bcc = BCC
                    mail.Subject = Subject

                    # iterate each attachment
                    iocimg = os.getcwd() + '/ioc.jpg'

                    attachments = mail.Attachments.Add(iocimg)
                    attachments.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                                                            "ioc.jpg")
                    mail.HTMLBody = Body
                    mail.Send()
                    try:
                        os.rename(maildirectory + "\\" + dirs, mailarchive + "\\" + dirs + "_" + str(timestr))
                    except:
                        mail_logging(" unable to move file to archive , deleting xml named " + dirs)
                        os.remove(maildirectory + "\\" + dirs)
                        continue
            time.sleep(10)
# ------------------------- CSC Template --------------------
    except:
        mail_logging(traceback.format_exc())
    finally:
        if cfg('/root/item[@key="Pid check"]').text:
            if cfg.pidfilecheck():
                print cfg('/root/item[@key="Exit"]').text
                cfg.pidfile.unlink()
                sys.exit()
# ------------------------- CSC Template --------------------