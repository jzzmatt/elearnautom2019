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

    query_params = {
        'device': name
    }
    
    device_netbx_dict = requests.get(
        NETBOX_URL + NETBOX_RESSOURCES['devices'],
        params=query_params,
        headers=HEADERS
    ).json()
    
    manufacturer = device_netbx_dict['result'][0]['device_type']['manufacturer']['name']
    device_model = device_netbx_dict['result'][0]['device_type']['model']

    if 'l2' in device_model.lower():
        device_type = "switch"
    else:
        device_type = "router"

    ip_addr_netbox_dict = requests.get(
         NETBOX_URL + NETBOX_RESSOURCES['devices'],
         params=query_params,
         headers=HEADERS
         ).json()['results']

    if manufacturer.low() == 'cisco':
        result.append('hostname {}'.format(name))
        for intf_dict in ip_addr_netbox_dict:
            interface_config_list = []
            interface_name = interface_dict["interface"]["name"]
            ip_address = IPv4Interface(interface_dict['address'])
            interface_config_list.append('ip address {} {}'.format(ip_address.ip, ip_address.netmask))
            interface_config = "\n".join(interface_config_list)
            result.append("interface {interface_name}\n{interface_config}\n!")
   
    return '\n'.join(result)
    #return json.dumps(ip_addr_netbox_dict, indent=4)

    





def main():
    print(create_device_config('SJ-SW1'))


if __name__ == '__main__':
    main()

