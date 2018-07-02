import win32com.client as win32
import MCC_OUTLOOK
import os
import pytz
from datetime import datetime
import csc.csclxmls
import path
# parameters
pth = path.path('XML/settings.xml')
settings = csc.csclxmls.node(pth)

# METHOD 1: Hardcode zones:
germantime = pytz.timezone('Europe/Amsterdam')
malaysiatime = pytz.timezone('Asia/Kuala_Lumpur')
fmt = '%Y-%m-%d %H:%M:%S'
msia = malaysiatime.localize(datetime.now())
german_ = msia.astimezone(germantime)
german = german_.strftime(fmt)

# outlook create item
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)

# iterate each attachment
iocimg = os.getcwd() + '/ioc.jpg'

attachments = mail.Attachments.Add(iocimg)
attachments.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                                         "ioc.jpg")

mail.To = settings('//item[@key="TO"]').text
mail.Cc = settings('//item[@key="CC"]').text
mail.Bcc = settings('//item[@key="BCC"]').text
mail.Subject = "MCC Active tickets : [{}/{}& {}] : CBI Critical / High & P1 Customer Tickets - CHECKED ON {} CET".format(
    MCC_OUTLOOK.CRIC, MCC_OUTLOOK.HIGH, len(MCC_OUTLOOK.P1), german)
mail.HTMLBody = open("finalhtml.txt",'r').read()
mail.display()
mail.send()
