import win32com.client as win32
import win32api
import psutil
import os
import subprocess
import path
import csc.csclxmls


# TODO: error handling , what ifs:
# TODO: attachment name exist but no file
# TODO: XML Corrupted, Requestor tag , if error go where and send to who . error log dialogue id.

# Drafting and sending email notification to senders. You can add other senders' email in the list
def send_outlookmail():
    """
     Name : send_outlookmail
     Description : To use outlook to send email.
     Prerequisites : outlook exe must be opened.
    """
    # getting xml path
    pth = path.path('mail.xml')
    mxml = csc.csclxmls.node(pth)

    # checking for xml embedintobody and convert all into list should it is node
    data = mxml('//item[@key="embedintobody"]')
    if isinstance(data, csc.csclxmls.nodelist):
        key = data
    else:
        # assign one node list
        key = [data]
    att = [] #attachment list for later  use
    body = [] #htmlbody list for later use

    # check if true or false to determine next step
    for text in key:
        # put html body
        puthtmlparent = text._parent
        puthtmlbody = puthtmlparent('item[@key="filename"]').text
        if text.text == "True":
            body.append(puthtmlbody)
        # put attachment mail. unlimited counts
        else:
            att.append(puthtmlbody)
    # read each .html file to string so can be place into htmlbody
    htmlread = ["<p>" + mxml('//item[@key="Body"]').text + "</p>"]
    for item in body:
        with open(item, 'r') as emailbody:
            htmlread.append(emailbody.read())
        emailbody.close()
    # outlook create item
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    # mail.SentOnBehalfOfName = "mailer@company.com"
    mail.To = mxml('//item[@key="To"]').text
    mail.Cc = mxml('//item[@key="Cc"]').text
    mail.Bcc = mxml('//item[@key="Bcc"]').text
    mail.Subject = mxml('//item[@key="Subject"]').text
    # compile string for html body below
    mail.HTMLBody =  "<br/>".join(htmlread)
    # iterate each attachment
    for attach in att:
        mail.Attachments.Add("C:\Users\ysiew\PycharmProjects\YSIEW\Toutlookmail\\" + attach)
        print attach
    mail.Send()
    #mail.display(True)



    # Open Outlook.exe. Path may vary according to system config
    # Please check the path to .exe file and update below

    # def open_outlook():
    #     try:
    #         subprocess.call(['C:\Program Files\Microsoft Office\Office15\Outlook.exe'])
    #         os.system("C:\Program Files\Microsoft Office\Office15\Outlook.exe");
    #     except:
    #         print("Outlook didn't open successfully")
    #
    #
    # # Checking if outlook is already opened. If not, open Outlook.exe and send email
    # for item in psutil.pids():
    #     p = psutil.Process(item)
    #     if p.name() == "OUTLOOK.EXE":
    #         flag = 1
    #         break
    #     else:
    #         flag = 0
    #
    # if (flag == 1):
    #     send_outlookmail()
    # else:
    #     open_outlook()
    #     send_outlookmail()

send_outlookmail()
