from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
import json
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

#print id[0]['IncidentID']['_value_1']


for x in id:
    inm = x.IncidentID._value_1
    print client.service.retrieveIncident(inm)