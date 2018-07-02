# from suds.client import Client
#
# url_service = 'https://xauto-dev.telekom.de:10502/ws/t00cc_sm9incidentmgmt.ws.provider.sm9IncidentManagement/TsiIncident_Port?wsdl'
# # uname = "INCIDENTMGMT-DPSMY"
# # Password = "inmMY2407x"
#
# client = Client(url_service ,)
#
#
# print client
import datetime
from dateutil.relativedelta import relativedelta
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
import requests_httpsproxy
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
#url_service = 'https://xauto-dev.telekom.de:10502/ws/t00cc_sm9incidentmgmt.ws.provider:sm9IncidentManagement?WSDL'
url_service = r'c:\temp\t00cc_sm9incidentmgmt.wsdl'
#url_service ="http://www.webservicex.net/ConvertSpeed.asmx?WSDL"
uname = "INCIDENTMGMT-DPSMY"
password = "inmMY2407x"


session = Session()
session.verify = False
session.auth = HTTPBasicAuth(uname, password)
#session.proxies = { "http": "tsl3isa.t-systems.co.uk:8080","https":"tsl3isa.t-systems.co.uk:8080"}
tp = Transport(session=session)
# session.get(url_service, transport=transport)
#client = Client(url_service ,transport=tp ,wsse=UsernameToken(uname, password))
client = Client(url_service ,transport=tp)
#
# years_ago = '2015-08-14T09:26:29+00:00'
# print years_ago

KLR = client.get_type('ns3:TsiIncidentModelType').attributes[0][1]
print KLR
#get_element('RetrieveTsiIncidentKeysListRequest')
print client.service.RetrieveTsiIncidentKeysList(KLR,"open.time >= tod() - '60 00:10:30'")

#print client.service.retrieveTsiIncidentTicketList(OpenedSince="2015-08-12 11:12:58 00:00")
# f = open("INM.json","w+")
# f.write(str(client.service.retrieveIncident("SIT0016986249")))
# f.close()
#print client.service.retrieveIncident("SIT0016986249")
