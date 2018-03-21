#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    two_by_two [options]

Options:
    -h, --help        Show this page
    --list
    --host=host
    --debug
    --verbose
"""
from docopt import docopt
import logging
import sys
import json

logger = logging.getLogger('two_by_two')


def natural_numbers():
    i = 0
    while True:
        yield i
        i += 1


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    data = {'_meta': {'hostvars': {}}}
    devices = ['Switch1',
               'Switch2',
               'Switch3',
               'Switch4']

    device_interface_seqs = {name: natural_numbers() for name in devices}
    all_links = set()

    for name in devices:
        links = []
        for remote_device in devices:
            if (name, remote_device) in all_links:
                continue
            if (remote_device, name) in all_links:
                continue
            if name == remote_device:
                continue
            links.append({'name': 'eth{0}'.format(next(device_interface_seqs[name])),
                          'remote_device_name': remote_device,
                          'remote_interface_name': 'eth{0}'.format(next(device_interface_seqs[remote_device]))
                          })
            all_links.add((name, remote_device))
            all_links.add((remote_device, name))
        host_data = {'ansible_topology': {'type': "switch", 'links': links}}
        data['_meta']['hostvars'][name] = host_data

    data['switches'] = devices

    print (json.dumps(data, sort_keys=True, indent=4))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))