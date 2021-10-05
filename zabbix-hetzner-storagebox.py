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

def validate_robot_ws(user, password):
    try:
        req = requests.get('https://robot-ws.your-server.de/storagebox', auth=(user, password))
        req.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('ERROR. More info: {}'.format(err))
        sys.exit(3)
    return True


def get_all_storage_box(user, password):
    try:
        req = requests.get('https://robot-ws.your-server.de/storagebox/', auth=(user, password))
        req.raise_for_status()
    except requests.exceptions.HTTPError:
        print('ERROR. Can\'t find any storage box')
    data = list()
    for item in req.json():
        if item and item["storagebox"]:
            if(item["storagebox"]["cancelled"] == False):
                data.append({"{#ID}": item["storagebox"]["id"], "{#LOGIN}": item["storagebox"]["login"],
                            "{#NAME}": item["storagebox"]["name"], "{#PRODUCT}": item["storagebox"]["product"]})
    return json.dumps({"data": data}, indent=4)

def get_storage_box_info(storage_box, user, password):
    try:
        req = requests.get('https://robot-ws.your-server.de/storagebox/' + storage_box, auth=(user, password))
        req.raise_for_status()
    except requests.exceptions.HTTPError:
        print('UNKNOWN - Can\'t find storage box (#{})'.format(storage_box))
    res = req.json()
    if(res["storagebox"] and res["storagebox"]["disk_quota"] and res["storagebox"]["disk_usage"]):
        percentage = '{0:.2f}'.format(100*(res["storagebox"]["disk_usage"] / res["storagebox"]["disk_quota"]))
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
        '-u',
        '--user',
        type=str,
        help='Enter the Hetzner Webservice username.',
    )
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        help='Enter the Hetzner Webservice password.',
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
    if args.user and args.password and validate_robot_ws(args.user,
                                              args.password):
        allStorageBoxes = list()
        if(args.discovery):
            allStorageBoxes = get_all_storage_box(args.user, args.password)
            print(allStorageBoxes)
        if(args.info):
            res = get_storage_box_info(args.info, args.user, args.password)
            print(res)
            print("\n\n\n")
            exit()
    else:
        parser.print_help()


if __name__ == '__main__':
    main(sys.argv[1:])
