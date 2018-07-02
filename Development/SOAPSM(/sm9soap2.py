from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
from threading import Thread
from datetime import datetime
a = datetime.now()

def datagather(x):
    inm = x.IncidentID._value_1
    datainm = client.service.retrieveIncident(inm)
    f = open(inm + ".txt", "w+")
    f.write(str(datainm))
    f.close()





url_service = r'c:\temp\t00cc_sm9incidentmgmt.wsdl'
uname = "INCIDENTMGMT-DPSMY"
password = "inmMY2407x"
session = Session()
session.verify=False
session.auth = HTTPBasicAuth(uname, password)
tp = Transport(session=session)
client = Client(url_service ,transport=tp)
# f = open("INM.json","w+")
# f.write(str(client.service.retrieveIncident("SIT0016986249")))
# f.close()
ra=client.get_element('ns3:RetrieveTsiIncidentKeysListRequest')
ras=ra(model={'instance':{'query':'status="closed"'},'keys':{}})
kk=client.service.RetrieveTsiIncidentKeysList(ras.model)

id = kk.keys


for x in id:
    t = Thread(datagather(x))
    t.start()

b = datetime.now()

c = b - a

print c.seconds