from win32com.client import Dispatch
import CND_CR8INM_0
import random
import os

# THIS GET DATA FROM OUTLOOK WITH SPECIFIC TITLE AND SAVE AS XLSX
# IT WILL THEN RUN CR8INM_0 TO TURN XLSX TO XML and SAVE AS NEW


outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder("6")
all_inbox = inbox.Items
donebox = inbox.Folders("AUTOCREATEARC")
sub_today = '[automationcreate]'
datafolder = '/INM/XLSXDATA/'
data= datafolder + "data_%s.xlsx" % random.randint(1,100000)
for msg in all_inbox:
    if msg.Subject == sub_today:
        for att in msg.Attachments:
            att.SaveAsFile(os.getcwd() + data)
        CND_CR8INM_0.generatexml(data)
        msg.Move(donebox)
        os.remove(os.getcwd() +data)



