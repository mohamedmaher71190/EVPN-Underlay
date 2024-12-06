import requests
from cvplibrary import CVPGlobalVariables, GlobalVariableNames, Device
import yaml

cvp_server = 'https://a24674-c90-1732805251-1-07af8278.topo.traininglabs.arista.com'
username = 'arista'
password = 'aristalt81'

# Login API Endpoint
login_url = "{}/web/login/authenticate.do".format(cvp_server)
login_payload = {"userId": username, "password": password}
login_response = requests.post(login_url, json=login_payload)
token = login_response.json().get("sessionId")
#print (token)
url="https://a24674-c90-1732805251-1-07af8278.topo.traininglabs.arista.com/cvpservice/configlet/getConfigletByName.do?name=MLAG%20Yaml"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer {}".format(token)}

response = requests.get(url, headers=headers)
raw=response.json()

Tags= CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)


for item in Tags: 
    #print (item)
    if item.startswith('hostname:'): 
       hostname = item.split(':')[1] 
       break



MLAG_yaml=raw['config']
MLAG=yaml.safe_load(MLAG_yaml)
Tags= CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)
#print (MLAG)
if "leaf" in hostname:
    print("interface ethernet 1")
    print("channel-group 100 mode active")
    print("no shutdown")
    print("interface ethernet 2")
    print("channel-group 100  mode active")
    print("no shutdown")
    print("interface port-Channel 100")
    print("switchport mode trunk")
    vlan=MLAG['odd']['vlan']
    domain=MLAG['odd']['domain']
    mlagtype=MLAG[hostname]['mlagtype']
    #print(mlagtype)
    print("vlan {}").format(vlan)
    print ("vlan 4093")
    print("trunk group MLAGPEER")
    print("interface port-Channel 100")
    print("switchport trunk group MLAGPEER")
    print("no spanning-tree vlan-id {}").format(vlan)
    print("interface vlan %s")% vlan
    if (mlagtype=="odd"):
      SVI= MLAG['odd']['svi']
      bgpsvi=MLAG['odd']['bgpsvi']
      peeradd=MLAG['odd']['peer']
      pri=10
    else:
      SVI= MLAG['even']['svi']
      bgpsvi=MLAG['even']['bgpsvi']
      peeradd=MLAG['even']['peer']
      pri=20
      
    print("ip address {}").format(SVI)
    print("no autostate")
    print("mlag configuration")
    print("local-interface vlan {}").format(vlan)
    print("peer-address {}").format(peeradd)
    print("peer-link port-Channel 100")
    print("domain-id {}").format(domain)
    print("interface vlan 4093")
    print("ip address {}").format(bgpsvi)
    print("no autostate")
     
    
    
    
    























