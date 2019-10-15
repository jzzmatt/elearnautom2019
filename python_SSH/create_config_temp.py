#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import requests
import json
import yaml
from pprint import pprint
from ipaddress import IPv4Interface
import sys
import time


NETBOX_URL = 'http://10.30.107.55:32770/api'
NETBOX_RESSOURCES = {
    'devices' : '/dcim/devices',
    'sites' : '/dcim/sites/',
    'ip_addresses': '/ipam/ip-addresses/',
    'interfaces': '/dcim/interfaces',
}

TOKEN = '0123456789abcdef0123456789abcdef01234567'
HEADERS = {
    "Authorization": "Token {}".format(TOKEN),
    "Content_Type": "application/json",
    "Accept": "application/json"
}

def create_device_config(name):
    '''
    return a Dictionnary of Devices
    '''
    result = []
    
    device_netbx_dict = requests.get(
        NETBOX_URL + NETBOX_RESSOURCES['devices'],
        params={'name': name},
        headers=HEADERS
    ).json()
    
    manufacturer = device_netbx_dict['results'][0]['device_type']['manufacturer']['name']
    device_model = device_netbx_dict['results'][0]['device_type']['slug'] #same as 'model'

    if 'l2' in device_model:
        device_type = "switch"
    else:
        device_type = "router"

    ip_addr_netbox_dict = requests.get(
         NETBOX_URL + NETBOX_RESSOURCES['ip_addresses'],
         params={'device': name},
         headers=HEADERS
         ).json()['results']

    # print(manufacturer)
    # print(device_model)
    # print(device_type)

    
    interfaces_dict = requests.get(
          NETBOX_URL + NETBOX_RESSOURCES['interfaces'],
          params={'device': name},
          headers=HEADERS
          ).json()['results']

    #pprint(interfaces_dict)


    if manufacturer.lower() == 'cisco':
        result.append('hostname {}\n!'.format(name))
        #Get Interface and interface Description
        for interface_dict in interfaces_dict:
              interface_config_list = []
              interface_name = interface_dict["name"]
              interface_dsc = " description {}".format(interface_dict["description"])
              print(interface_name)
        #Get Ip address and MASK
        for ip in ip_addr_netbox_dict:
            if ip['interface']['device']['name'] == name:
                if ip['interface']['name'] == interface_name:
                    ip_address = IPv4Interface(ip['address'])
                    print(ip_address)
   
    #         ip_address = IPv4Interface(interface_dict["address"])
    #         interface_config_list.append(' ip address {} {}'.format(ip_address.ip, ip_address.netmask))

    #         for interface in interfaces_dict:
    #             #   interface_dsc = " description {}".format(interface['description'])    
    #             if interface['name'] == interface_name and (interface['form_factor']['label'] != "Virtual"):
    #                     interface_config_list.append(' no switchport')

    #         interface_config_list.append(' no shutdown')
    #         interface_config = "\n".join(interface_config_list)
    #         result.append("interface {}\n{}\n{}\n!".format(interface_name,interface_dsc,interface_config))
   
    # return '\n'.join(result)
    #return json.dumps(ip_addr_netbox_dict, indent=4)


def main():
    create_device_config('SJ-SW1')


if __name__ == '__main__':
    main()

