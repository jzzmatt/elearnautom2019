#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import requests
import json
import yaml
import pprint import pprint
import argparse
import sys
import netaddr

NETBOX_URL = 'http://192.168.122.116/api'
NETBOX_RESSOURCES = {
    'devices' : '/dcim/devices',
    'sites' : '/dcim/sites/',
    'ip_addresses': '/ipam/ip-addresses/',
    'interfaces': '/dcim/interfaces',
}

TOKEN = ''
HEADERS = {
    'Authorization': 'Token {}'.format(TOKEN),
    'Content_Type': 'application/json',
    'Accept': 'application/json'
}

def netbox_query(resources, query_params=None):
    return requests.get(
        NETBOX_URL + NETBOX_RESSOURCES[resources], params=query_params, headers=HEADERS
    )

nbx_devices = netbox_query('devices')

pprint(nbx_devices)
