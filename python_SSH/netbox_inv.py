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

NETBOX_URL = 'http://192.168.122.116:8000/api'
NETBOX_RESSOURCES = {
    'devices' : '/dcim/devices',
    'sites' : '/dcim/sites/',
    'ip_addresses': '/ipam/ip-addresses/',
    'interfaces': '/dcim/interfaces',
}


TOKEN = '91e9482beba078638f98f936bdbf8b745bcd0dce'
HEADERS = {
    'Authorization': 'Token {}'.format(TOKEN),
    'Content_Type': 'application/json',
    'Accept': 'application/json'
}

SITES = [
    {'name': 'LUENA', 'slug': 'luen'}, 
    {'name': 'HUAMBO', 'slug': 'huamb'}

]


SITES_IDS = {
    ''
}

def netbox_query(resources, query_params=None):
    '''
    Perform a Simple Query to Netbox via Device API
    '''
    return requests.get(
        NETBOX_URL + NETBOX_RESSOURCES[resources], params=query_params, headers=HEADERS
    )


def nbx_add_site(name, slug):
    '''
    Manualy Add a Device from a Yaml Inventory to Netbox API 
    '''
    data = {
        'name' : name,
        'slug' : slug,
    }
    req = requests.post(NETBOX_URL + NETBOX_RESSOURCES['sites'], headers=HEADERS, json=data)
    if req.status_code == 200 or req.status_code == 201:
        #200 => mean sucess
        print('==>Site {} was created Successfully'.format(name))
    else:
        req.raise_for_status()


def push_sites_to_api():
    '''
    Add sites from Sites Dictionnary to NetBOX API
    '''
    for site in SITES:
        nbx_add_site(**site)
        print("site {} created !!".format(site['name']))
        time.sleep(1)


def get_nbx_site_id(resources, query_params=None):
    return requests.get(NETBOX_URL + NETBOX_RESSOURCES[resources],params=query_params, headers=HEADERS)


def nbx_add_device(name, device_type_id, site_id, device_role_id):
    '''
    name: name of the Device . eg SW1
    device_type_id: CSR1000v, C6500 #this is match or link to manufacture, here is #2
    site_id: site_id here is #1
    device_role_id: eg CORE-Switch, Edge, Access-Switch
    '''
    data = {
        'name': name,
        'display_name': name,
        'device_type': device_type_id,
        'device_role': device_role_id,
        'site': site_id,
        'status': 1
    }


def main():
    #nbx_devices = netbox_query('devices')
    #print(nbx_devices)
    sites_dicts = get_nbx_site_id('sites')
    print(sites_dicts)
    #push_sites_to_api()

if __name__ == '__main__':
    main()

