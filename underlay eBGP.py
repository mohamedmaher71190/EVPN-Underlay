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
url="https://a24674-c90-1732805251-1-07af8278.topo.traininglabs.arista.com/cvpservice/configlet/getConfigletByName.do?name=myunderlay"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer {}".format(token)}

response = requests.get(url, headers=headers)
raw=response.json()
underlay_yaml=raw['config']
underlay=yaml.safe_load(underlay_yaml)
Tags= CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)


for item in Tags: 
    #print (item)
    if item.startswith('hostname:'): 
       hostname = item.split(':')[1] 
       if "DC1" in hostname:
         DC= "DC1"
       else: 
         DC ="DC2"
       
       if "borderleaf" in hostname:
         type= "borderleafs"
       else:
         if "leaf" in hostname:
           type= "leafs"
         else: 
           if "spine" in hostname:
               type= "spines"
               
       
       break
     
     
def gen_ips():
    for interface,ip  in underlay[DC][type][hostname]['interfaces'].items():
      print("int {}".format(interface))
      print("no switchport")
      print("ip address {}/{}".format(ip['ipv4'], ip['mask']))
      print ("mtu {}").format(underlay['global']['mtu'])
      
    for loopback,ip  in underlay[DC][type][hostname]['loopbacks'].items():
      print("int {}".format(loopback))
      print("ip address {}/{}".format(ip['ipv4'], ip['mask']))
asn= underlay[DC][type][hostname]['asn']
lo0= underlay[DC][type][hostname]['loopbacks']['loopback0']['ipv4']
if 'loopback1' in underlay[DC][type][hostname]['loopbacks']:
    lo1 = underlay[DC][type][hostname]['loopbacks']['loopback1']['ipv4']
    
def bgp_underlay():

    print("ip routing")
    print("service routing protocols model multi-agent")
    print ("router bgp {}").format(asn)
    print ("router-id {}").format(lo0)
    print("maximum-paths 4 ecmp 4")
    print("distance bgp 20 200 200")
    print("no bgp default ipv4-unicast") 
    print("bgp log-neighbor-changes")  
    print("neighbor underlay  peer group")
    data=underlay[DC][type][hostname]['bgp']
    #print(data)
    
    for peer, remote_as in zip(data['peers'], data['remote-as']):
      print("neighbor {} remote-as {}").format(peer,remote_as)
      print("neighbor {} allowas-in 1").format(peer)
      print ("neighbor {} maximum-routes 12000").format(peer)
      print ("neighbor {} peer group underlay").format(peer)
    if "leaf1" in hostname and 'leaf' in type: 
      print("neighbor 172.16.255.2 remote-as {}").format(asn)
    if "leaf2" in hostname and  'leaf' in type: 
      print("neighbor 172.16.255.1 remote-as {}").format(asn)
    print ("address-family ipv4")
    print("neighbor underlay activate")
    print("network {}/32").format(lo0)
    if 'loopback1' in underlay[DC][type][hostname]['loopbacks']:
       print("network {}/32").format(lo1)
def bgp_overlay():
    print ("router bgp {}").format(asn)
    print("neighbor overlay peer group") 
    if 'spine' in hostname:
       for switch,switchdetails  in underlay[DC]['leafs'].items():
          overlayneighorip=switchdetails['loopbacks']['loopback0']['ipv4']
          overlayneighboras= switchdetails['asn']
          print ("neighbor {} remote-as {}").format(overlayneighorip,overlayneighboras)
          print ("neighbor {} peer group overlay").format(overlayneighorip)
          
       for switch,switchdetails  in underlay[DC]['borderleafs'].items():
          overlayneighorip=switchdetails['loopbacks']['loopback0']['ipv4']
          overlayneighboras= switchdetails['asn']
          print ("neighbor {} remote-as {}").format(overlayneighorip,overlayneighboras)
          print ("neighbor {} peer group overlay").format(overlayneighorip)
       print("neighbor overlay next-hop-unchanged")
          
    if 'leaf' in hostname:
       for switch,switchdetails  in underlay[DC]['spines'].items():
          overlayneighorip=switchdetails['loopbacks']['loopback0']['ipv4']
          overlayneighboras= switchdetails['asn']
          print ("neighbor {} remote-as {}").format(overlayneighorip,overlayneighboras)
          print ("neighbor {} peer group overlay").format(overlayneighorip)
    
    print("neighbor overlay send-community extended")
    print("neighbor overlay ebgp-multihop 3")
    print("neighbor overlay update-source loopback 0")
    print("neighbor overlay maximum-routes 0") 
    print("address-family evpn")
    print("neighbor overlay activate")
    
    
gen_ips()
bgp_underlay()
bgp_overlay()
