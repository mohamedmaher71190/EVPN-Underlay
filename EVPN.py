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
url="https://a24674-c90-1732805251-1-07af8278.topo.traininglabs.arista.com/cvpservice/configlet/getConfigletByName.do?name=EVPN%20Yaml"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer {}".format(token)}

response = requests.get(url, headers=headers)
raw=response.json()
EVPN_yaml=raw['config']
EVPN=yaml.safe_load(EVPN_yaml)
Tags= CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)


for item in Tags: 
    #print (item)
    if item.startswith('hostname:'): 
       hostname = item.split(':')[1] 
       break
     
     

vrf= EVPN[hostname]['vrf']
vrfVNI=EVPN[hostname]['vrf-VNI']
lo0=EVPN[hostname]['lo0']
lo1=EVPN[hostname]['lo1']
vmac=EVPN[hostname]['vMAC']
asn= EVPN[hostname]['asn']
print("vrf instance {}").format(vrf)
print("ip routing vrf {}").format(vrf)
print("ip virtual-router mac-address {}").format(vmac)

#for vlan in EVPN[hostname]['vlans']:
  #print (EVPN[hostname]['vlans'][vlan]['tag'])
  

for vlan,details in EVPN[hostname]['vlans'].items():
  tag= details['tag']
  l2VNI=details['VNI']
  SVI=details['SVI']
  SVIV=details['SVIV']
  print("vlan {}").format(tag)
  print("interface vlan {}").format(tag)
  print("no autostate")
  print("vrf {}").format(vrf)
  print(" ip virtual-router address {}").format(SVIV)
  print("ip address {}").format(SVI)
  print("router bgp {}").format(asn)
  print("vlan {}").format(tag)
  print("rd {}:{}").format(lo0,l2VNI)
  print("route-target both {}:{}").format(tag,l2VNI)
  print(" redistribute learned")
  print("interface Vxlan1")
  print(" vxlan vlan {} vni {}").format(tag,l2VNI)
  
print("router bgp {}").format(asn)
print("vrf {}").format(vrf)
print("rd {}:{}").format(lo0,vrfVNI)
print("route-target export evpn {}:{}").format(vrfVNI,vrfVNI)
print("route-target import evpn {}:{}").format(vrfVNI,vrfVNI)
print("redistribute connected")
print("interface Vxlan1")
print("vxlan source-interface loopback1")
print(" vxlan virtual-router encapsulation mac-address {}").format(vmac)
print("vxlan udp-port 4789")
print( "vxlan vrf  {}  vni {}").format(vrf,vrfVNI)


  
  

  
  
  
  
  
  

     
