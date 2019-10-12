#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import requests
import json
import yaml
from pprint import pprint
import argparse
import sys
import netaddr
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
    "Accept": "application/json ;indent=4"
}

def create_device_config(name):
    result = []
    query_params = {
        'devices': name
    }
    ip_addr_netbox_dict = requests.get(
         NETBOX_URL + NETBOX_RESSOURCES['devices'],
         params=query_params,
         headers=HEADERS
         )
    return json.dumps(ip_addr_netbox_dict, indent=4)



def main():
    print(create_device_config('SJ-SW1'))


if __name__ == '__main__':
    main()

