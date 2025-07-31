#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import requests
import json

__author__ = 'Luca Salvestrini'
__copyright__ = 'Copyright 2021'
__license__ = 'MIT'
__version__ = '1.0'
__maintainer__ = 'Luca Salvestrini'
__email__ = 'laky1694@gmail.com'

def validate_robot_ws(api_token):
    try:
        headers = {"Authorization": "Bearer " + api_token}    
        req = requests.get('https://api.hetzner.com/v1/storage_boxes', headers=headers)
        req.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('ERROR. More info: {}'.format(err))
        sys.exit(3)
    return True


def get_all_storage_box(api_token):
    try:
        headers = {"Authorization": "Bearer " + api_token}
        req = requests.get('https://api.hetzner.com/v1/storage_boxes', headers=headers)
        req.raise_for_status()
    except requests.exceptions.HTTPError:
        print('ERROR. Can\'t find any storage box')
    data = list()
    response_json = req.json()['storage_boxes']
    for item in response_json:
        if item and item["status"] == 'active':
                data.append({"{#ID}": item["id"], "{#LOGIN}": item["username"],
                            "{#NAME}": item["name"], "{#PRODUCT}": item["storage_box_type"]["description"]})
    return json.dumps({"data": data}, indent=4)

def get_storage_box_info(storage_box, api_token):
    try:
        headers = {"Authorization": "Bearer " + api_token}
        req = requests.get('https://api.hetzner.com/v1/storage_boxes/' + str(storage_box), headers=headers)
        req.raise_for_status()
    except requests.exceptions.HTTPError:
        print('UNKNOWN - Can\'t find storage box (#{})'.format(storage_box))
    res = req.json()
    if(res["storage_box"] and res["storage_box"]["stats"]["size_data"] and res["storage_box"]["storage_box_type"]["size"]):
        percentage = '{0:.2f}'.format(100*(res["storage_box"]["stats"]["size_data"] / res["storage_box"]["storage_box_type"]["size"]))
        return percentage
    return False

def main(args):
    parser = argparse.ArgumentParser(
        description='\
        Zabbix template to discover and monitor Hetzner Storage Boxes.',
    )

    parser.add_argument(
        '-s',
        '--storage-box',
        dest='storage_box',
        type=str,
        help='Enter the Storage Box ID.',
    )
    parser.add_argument(
        '-t',
        '--token',
        dest='api_token',
        type=str,
        help='Enter the Hetzner API Token.',
    )
    
    parser.add_argument(
        '-d',
        '--discovery',
        dest='discovery',
        action='store_true',
        help='Optional parameter to discover only',
    )

    parser.add_argument(
        '-i',
        '--info',
        dest='info',
        type=str,
        help='Optional parameter to get info only',
    )

    args = parser.parse_args()
    
    if args.api_token and validate_robot_ws(args.api_token):
        allStorageBoxes = list()
        if(args.discovery):
            allStorageBoxes = get_all_storage_box(args.api_token)
            print(allStorageBoxes)
        if(args.info):
            res = get_storage_box_info(args.info, args.api_token)
            print(res)
            print("\n\n\n")
            exit()
    else:
        parser.print_help()


if __name__ == '__main__':
    main(sys.argv[1:])
