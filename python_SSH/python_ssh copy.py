#!/usr/bin/env python
#Application Write by Ktbyers , uses a categories of IOS for applied facts and some modules
#http://github.com/Ktbyers/netmiko/blob/develop/README.md

import netmiko
import yaml
import asyncio
import netdev
from copy import deepcopy
from pprint import pprint

COMMAND_LST = [
    'show clock',
    'show version | inc IOS',
    'show ip int br',

]

def read_pyaml(path='inventory.yml'):
    '''
    Reads inventory yaml and return dictionnary with parsed yamls
    '''
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

async def collect_outps(device_params, commands):
    '''
    args:
       devices: dict of Devices or Host, where key is the hostname, value is netmiko connection dictionary
       commands: (list of commands)

    returns:
       dict: key is the hostname, value is the string of all outputs
    '''
    hostname = device_params.pop('hostname')
    async with netdev.create(**device_params) as connection:
        device_result = ['{0} {1} {0}'.format('='* 20, hostname)]

        for command in commands:
            command_result = await connection.send_command(command)
            device_result.append('{0} {1} {0}'.format('='* 20, command))
            device_result.append(command_result)

        device_result_string = '\n\n'.join(device_result)
        return device_result_string


def main():
   parsed_yaml = read_pyaml()
   loop = asyncio.get_event_loop()
   tasks = [loop.create_task(collect_outps(device, COMMAND_LST)) 
            for device in from_connection_params_from_yaml(parsed_yaml, site="SJ-HQ")]
   loop.run_until_complete(asyncio.wait(tasks))

   for task in tasks:
       print(task.result())

   

 


if __name__ == '__main__':
    main()