import pandas as pd
import path
import time
import csc.csclxmls
import os

# THIS CREATE PRIORITY BASED ON THE PRIORITY GIVEN BY EXCEL
def prioritycheck(data):
    if data == "P5":
        return "NONE" , "NONE"
    elif data == 'P4':
        return "LOW", "LOW"
    elif data == 'P3':
        return "MEDIUM", "MEDIUM"
    elif data == 'P2':
        return "HIGH", "HIGH"
    else:
        return "CRITICAL", "CRITICAL"
# THIS CONVERT XLSX INTO XML
def generatexml(data):
    File = os.getcwd() + data
    df = pd.read_excel(File, sheetname='Sheet1')

    pth = path.path('XML/settings.xml')
    settings = csc.csclxmls.node(pth)
    CRIC ,RESTRICTION = prioritycheck(df['PRIORITY'][0])

    Mandakey = ["TITLE","CUSTOMER","CATEGORY1","CATEGORY2","AG","CRIC","RESTRICTION","CI","WIW","DESCRIPTION"]
    timekey = ["ticketsent","ticketcreated","ticketfail"]
    mandaitemlist = [
        df['TITLE'][0],
        "",
        "DETAILED CATEGORIES",
        "SERVER",
        df['AG'][0],
        CRIC,
        RESTRICTION,
        df['CI'][0],
        settings('//item[@key="WIW"]').text,
        df['DESCRIPTION'][0]
    ]

    pth = path.path('INM/NEW/INM_%d.xml' % time.time())
    # create xml file with <root/> before initiate below
    INMroot = csc.csclxmls.node('<root/>')

    SM9field = INMroot + "SM9"
    SM9item = SM9field + 'item'
    SM9item['key'] = 'INCIDENTID'
    SM9item.text = ""

    i= 0
    Mandafield = SM9field + "Mandatory"
    for x in Mandakey:
        Mandaitem= Mandafield + 'item'
        Mandaitem['key'] = x
        Mandaitem.text = mandaitemlist[i]
        i+= 1

    timefield = INMroot + "time"
    for x in timekey:
        timeitem = timefield + 'item'
        timeitem['key'] = x
        timeitem.text = ""

    INMroot.write(pth)