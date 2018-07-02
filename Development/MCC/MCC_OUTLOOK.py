import pandas as pd
import pytz
import os


# Functions

def places(data):
    for y in PLACENAME:
        for x in data:
            if any(i in data[x][3] for i in PLACENAME[y]):
                data[x].insert(0, y)
                yield data[x]


def tablecreation(data, data2):
    border = "<tr>"
    for x, y in zip(COLUMNWIDTH, HEADER):
        border += "<th id='header' width='{}'>{}</th>".format(x, y)
    border += "</tr>"

    tb = "<table><tr id='border'><td colspan='9' id='head'><p> CBI CRITICAL & HIGH </i></p><br/></td></tr>" + border
    if len(data) >= 1:
        changecolor = True
        for x in places(data):
            if changecolor:
                st = "<tr bgcolor='#d0d3c0' ><td id='para'>"
                changecolor = False
            else:
                st = "<tr><td id='para'>"
                changecolor = True
            st += "</td><td id='para'>".join(x).encode('utf-8')
            st += "</td></tr>"
            tb += st

    else:
        st = "<tr><td id='NA'> NA <br/> </td></tr>"
        tb ="<table><tr id='border'><td colspan='9' id='head'><p> CBI CRITICAL & HIGH </i></p><br/></td></tr>" + st
    final = tb
    tb2 = "<tr><td colspan='9' id='head'><br/><p> PRIORITY 1 </p><br/></td></tr>" + border
    if len(data2) >= 1:
        changecolor2 = True
        for y in places(data2):
            if changecolor2:
                st2 = "<tr bgcolor='#d0d3c0' ><td id='para'>"
                changecolor2 = False
            else:
                st2 = "<tr><td id='para'>"
                changecolor2 = True
            st2 += "</td><td id='para'>".join(y).encode('utf-8')
            st2 += "</td></tr>"
            tb2 += st2
    else:
        st2 = "<tr><td id='NA'> NA <br/> </td></tr>"
        tb2 = "<tr><td colspan='9' id='head'><br/><p> PRIORITY 1 </p><br/></td></tr>" + st2
    final += tb2 + "</table>"
    return final


# PARAMETERS
Folder = "C:/MCC/"
Pending = Folder + "Pending/"
File = "MCC_DATA.xlsx"
df = pd.read_excel(Folder + File, sheetname='Sheet1')
fmt = '%Y-%m-%d %H:%M:%S'
if not os.path.exists(Pending):
    os.makedirs(Pending)
# METHOD 1: Hardcode zones:
germantime = pytz.timezone('Europe/Amsterdam')
malaysiatime = pytz.timezone('Asia/Kuala_Lumpur')

# PLACES CRITERIA
PLACENAME = {"GERMANY": ["C.SAP.DE"],
             "HUNGARY": ["C.SAP.HU"],
             "MALAYSIA": ["C.SAP.MY", "C.SAP.SG"],
             "MEXICO": ["C.SAP.MX"],
             "SLOVAKIA": ["C.SAP.INT", "C.SAP.SK", "CS.EMEA"],
             "LBU": ["C.SAP.BR", "C.SAP.ZA"]}
HEADER = ["Countries", "Incident ID", "Prio", "Status", "Assignment", "Customer", "CBI", "TSI Creation Date (CET) ", "Title"]
COLUMNWIDTH = ['46.0px', '62.0pt', '22.0px', '72.0px', '125.0px', '167.0px', '38.0px', '109.0px', '*']
PCRITICAL = {}
P1 = {}
INMdata = []
CRIC = 0
HIGH = 0
i = 1
j = 1
# data processing
for index, row in df.iterrows():
    msia = malaysiatime.localize(row[6])
    german_ = msia.astimezone(germantime)
    german = german_.strftime(fmt)
    prio = row[1][0]
    if "Pending Customer" in row[2] and row[0] not in os.listdir(Pending):
        os.makedirs(Pending + row[0])
        if row[5] == "HIGH":
            PCRITICAL[i] = [row[0], prio, row[2], row[3], row[4], row[5], german, row[7]]
            HIGH += 1
        elif row[5] == "CRITICAL":
            PCRITICAL[i] = [row[0], prio, row[2], row[3], row[4], row[5], german, row[7]]
            CRIC += 1
        else:
            P1[j] = [row[0], prio, row[2], row[3], row[4], row[5], german, row[7]]
    elif "Pending Customer" in row[2] and row[0] in os.listdir(Pending):
        pass
    else:

        if row[5] == "HIGH":
            PCRITICAL[i] = [row[0], prio, row[2], row[3], row[4], row[5], german, row[7]]
            HIGH += 1
        elif row[5] == "CRITICAL":
            PCRITICAL[i] = [row[0], prio, row[2], row[3], row[4], row[5], german, row[7]]
            CRIC += 1
        else:
            P1[j] = [row[0], prio, row[2], row[3], row[4], row[5], german, row[7]]
    i += 1
    j += 1

# clear pending folder
for data in df[df.columns[0]]:
    INMdata.append(data)
for data_ in os.listdir(Pending):
    if data_ not in INMdata:
        os.rmdir(Pending + data_)
# CSS

css = """ <style> 
        #word {
            font-size:14;
            font-family:calibri;   
        }
        #header {
            color: white;
            border:solid black 1.0pt;
            
            background:#E20074;
            font-size:9pt;
            font-family:"Tahoma","sans-serif";
        }
        #para {
           color: black;
           border:solid black 1.0pt;
           
           font-size:9pt;
           
        } 
        #NA {
           color: black;
           font-weight:bold;
           
           font-size:14pt;
           
        } 
        table{
            border-collapse: collapse;
        }
        #head {
           color:#e20074; 
           font-size:16;
           font-weight:bold;
           
        } 
        </style>"""

table = tablecreation(PCRITICAL, P1)

fullemail = "<head>" + css + "</head>"
fullemail += """<center><img src='cid:ioc.jpg' height=115 width=540></center><br><body><p id='word'>Dear All,<br/></p><p id='word'>See below for the list of active incident tickets. take appropriate action immediately
 to ensure tickets are not breached.<br></p>"""
fullemail += "<div>" + table + "</div><br/>"
fullemail += """<p id='word'><br> ** The pending Customer Tickets will be deleted from the next Report.</p></body>"""

# tablecritical = tablecreation(PCRITICAL)
# tablep1 = tablecreation(P1)
#
# fullemail = "<head>" + css + "</head>"
# fullemail += """<center><img src='cid:ioc.jpg' height=115 width=540></center><br><body><p>Dear All,<br/></p><p>See below for the list of active incident tickets. take appropriate action immediately
#  to ensure tickets are not breached.<br></p><font color=#e20074><p style='font-size:16'><b><i> CBI CRITICAL & HIGH </i></b></p></font> """
# fullemail += "<div>" + tablecritical + "</div><br/>"
# fullemail += "<font color=#e20074><p style='font-size:16;'><b> PRIORITY 1 </b></p></font>"
# fullemail += "<div>" + tablep1  + "</div><br/>"
# fullemail += """<p><br> ** The pending Customer Tickets will be deleted from the next Report.</p></body>"""

html = open("finalhtml.txt", "w+")
html.write(fullemail)
html.close()
# html2 = open("finalhtml.html", "w")
# html2.write(fullemail)
# html2.close()
