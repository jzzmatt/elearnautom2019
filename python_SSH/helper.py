#!/usr/bin/env python
#Application Write by Ktbyers , uses a categories of IOS for applied facts and some modules
#http://github.com/Ktbyers/netmiko/blob/develop/README.md
#https://github.com/dmfigol/network-programmability-stream/blob/master/helper.py

import yaml
from copy import deepcopy
from pprint import pprint

SITES = {
    "san-jose": 3,
    "bruxels" : 4
}

DEVICE_TYPES = {
    'CSR1000v': 1,
    'IOSv-L2' : 2,
}

DEVICE_ROLES = {
    'access': 1,
    'edge': 2,
    'core': 3
}

def read_pyaml(path='inventory.yml'):
    '''
    Reads inventory yaml and return dictionnary with parsed yamls
    '''
    with open(path) as file:
        yaml_content = yaml.load(file)
    return yaml_content

def from_connection_params_from_yaml(format_yaml, site_name=None):
    '''
    From Dictionnary comming from parsed yaml, 
    Args:
       parsed_yaml : dictionnary with parsed yamls file
       site : string site name , by default takes 'all'

    Returns: dict connection parameters for netmiko
    '''
    parsed_yaml = deepcopy(format_yaml) 
    global_params = parsed_yaml['all']['vars']
    found = False
    for site_dict in parsed_yaml['all']['sites']:
        if not site_name or site_dict['name'] == site_name:
            for host in site_dict['hosts']:
                host_dict = {}
                if "device_type_netmiko" in host:
                    host['device_type'] = host.pop('device_type_netmiko')
                host_dict.update(global_params)
                host_dict.update(host)
                host_dict.pop('device_role')

                found = True
                yield host_dict
                
    if site_name is not None and not found:
        raise KeyError("Site {} is not specified in inventory YAMLS".format(site_name))

def from_device_params_from_yaml(parsed_yaml):
    parsed_yaml = deepcopy(parsed_yaml)
    for site_dict in parsed_yaml['all']['sites']:
        site_name = site_dict['name']
        site_id = SITES.get(site_name)
        for host_dict in site_dict['hosts']:
            device_params = dict()
            device_params["name"] = host_dict["hostname"]
            device_params["display_name"] = host_dict["hostname"]
            device_params["site"] = site_id
            device_params["device_type"] = DEVICE_TYPES.get(host_dict.get("device_type"))
            device_params["device_role"] = DEVICE_ROLES.get(host_dict.get("device_role"))
            device_params["status"] = 1
            yield device_params
