#!/usr/bin/env python
#Application Write by Ktbyers , uses a categories of IOS for applied facts and some modules
#http://github.com/Ktbyers/netmiko/blob/develop/README.md

import netmiko
import yaml
from copy import deepcopy
from pprint import pprint

COMMAND_LST = [
    'show clock',
    'show version | inc IOS',
    'show ip int br',

]

def read_pyaml(path='inventory.yml'):
    with open(path) as file:
        yaml_content = yaml.load(file)
    return yaml_content

def from_connection_params_from_yaml(format_yaml, site='all'):
    '''
    From Dictionnary comming from parsed yaml, 
    Args:
       parsed_yaml : dictionnary with parsed yamls file
       site : string site name , by default takes 'all'

    Returns: dict connection parameters for netmiko
    '''
    parsed_yaml = deepcopy(format_yaml) 
    result = {}
    global_params = parsed_yaml['all']['vars']
    site_dict = parsed_yaml['all']['groups'].get(site)
    if not site_dict:
        raise KeyError("Site {} is not specified in inventory YAMLS".format(site))

    for device in site_dict['hosts']:
        host_dict = {}
        #hostname = device.pop('hostname')
        host_dict.update(global_params)
        host_dict.update(device)
        yield host_dict
        #result[hostname] = host_dict
    #return result

def collect_outps(devices, commands):
    '''
    args:
       devices: dict of Devices or Host, where key is the hostname, value is netmiko connection dictionary
       commands: (list of commands)

    returns:
       dict: key is the hostname, value is the string of all outputs
    '''
    for device in devices:
        hostname = device.pop('hostname')
        connection = netmiko.ConnectHandler(**device)
        device_result = ['=' * 20 + hostname + '=' * 20]
        for command in commands:
            command_result = connection.send_command(command)
            device_result.append('=' * 20 + command_result + '=' * 20)
        device_result_string = '\n\n'.join(device_result)
        yield device_result_string


def main():
    #print(read_pyaml())
    #pprint(from_connection_params_from_yaml(read_pyaml(), "SJ-HQ"))
    connection_params = from_connection_params_from_yaml(read_pyaml(), "SJ-HQ")
    for device_result in collect_outps(connection_params, COMMAND_LST):
        print(device_result)
    

 


if __name__ == '__main__':
    main()