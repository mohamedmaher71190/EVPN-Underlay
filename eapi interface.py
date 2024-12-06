
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
    for intname, intip in switchdetails['interfaces'].items():
       #print (intip)
        Connect.api("ipinterfaces").create(intname)
        Connect.api("ipinterfaces").set_address(intname,intip)
        eth=Connect.api("ipinterfaces").get(intname)
        print(eth)
