
#! /usr/bin/python3
import yaml
file = open('/home/coder/project/persist/YAML/example.yaml', 'r' )
example_raw =  file.read()
example_yaml = yaml.safe_load(example_raw)
#print(example_yaml)
import pyeapi
for switch,switchdetails in example_yaml['switch'].items():
    #print (switch)
    Connect= pyeapi.connect_to(switch)
    for vlan in switchdetails['vlans']:
       #print (vlan)
        Connect.api("vlans").create(vlan)
        #Connect.api("ipinterfaces").set_address(intname,intip)
        showvlan=Connect.api("vlans").getall()
        print(showvlan)
