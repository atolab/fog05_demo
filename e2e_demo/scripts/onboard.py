#!/usr/bin/env python3

import sys
from fog05 import API
from fog05 import Schemas
import os
import json
from jsonschema import validate, ValidationError
import uuid


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(entity_path):
    a = API(endpoint='192.168.86.44')
    e_manifest = json.loads(read_file(entity_path))
    #p_manifest = json.loads(read_file('./native_plugin.json'))

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {} | Name: {}'.format(n[0], n[1]))

    input("Press enter to continue")

    # print('Adding Native plugin to all node')
    # for n in nodes:
    #     u = n[0]
    #     a.plugin.add(manifest=p_manifest,node_uuid=u)

    #print('Node plugins')
    # for n in nodes:
    #    u = n[0]
    #    print('Node {}:'.format(u))
    #    pls = a.plugin.list(node_uuid=u)
    #    print('## {}'.format(pls))
    #input("Press enter to continue")

    infos = a.add(e_manifest)
    print('Onboarded:')
    for k in infos.get('networks'):
        print('Network: {}'.format(k))
    print('#########################')
    for k in infos.get('entity'):
        print('Entity: {}'.format(k))
        for k1 in infos.get('entity').get(k):
            print('|-Atomic Entity: {}'.format(k1))
            print('  |- Instance: {}'.format(infos.get('entity').get(k).get(k1)))

    input("press enter to offload")
    a.remove(e_manifest.get('uuid'))
    print('{} Offloaded'.format(e_manifest.get('uuid')))
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[Usage] {} <path to entity manifest>'.format(sys.argv[0]))
        exit(0)
    main(sys.argv[1])
