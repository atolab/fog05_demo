from fog05 import FIMAPI
import uuid
import json
import sys
import os


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, fdufile, fdu2file,  n1, n2):
    a = FIMAPI(ip)

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {}'.format(n))

    fdu_d = json.loads(read_file(fdufile))
    fdu2_d = json.loads(read_file(fdu2file))

    e_uuid = fdu_d.get('uuid')
    e2_uuid = fdu2_d.get('uuid')
    #n1 = '90c02ec42f2a47448d5f8e33ad7bf7e2'
    #n2 = '297b270c79eb45089b6979f86fbdaa96'
    #n1 = '21e48018-d4c3-499e-baee-6990e33a6c0c'

    input('press enter to onboard descriptors')
    a.fdu.onboard(fdu_d)
    a.fdu.onboard(fdu2_d)
    input('Press enter to define')
    i1 = a.fdu.define(e2_uuid, n2)
    i2 = a.fdu.define(e_uuid, n1)
    #a.entity.define(e_manifest, n2, wait=True)
    input('Press enter to configure')
    a.fdu.configure(i1)
    a.fdu.configure(i2)
    input('Press enter to run')
    a.fdu.start(i1)
    a.fdu.start(i2)

    # input('Press enter to stop')
    # a.entity.stop(e_uuid, n1, i_uuid, wait=True)
    # input('Press enter to clean')
    # a.entity.clean(e_uuid, n1, i_uuid, wait=True)
    # input('Press enter to undefine')
    # a.entity.undefine(e_uuid, n1, wait=True)

    # input('Press enter to migrate')

    #res = a.entity.migrate(e_uuid, i_uuid, n1, n2, wait=True)
    #print('Res is: {}'.format(res))
    input('Press enter to remove')
    a.fdu.stop(i1)
    a.fdu.stop(i2)
    a.fdu.clean(i1)
    a.fdu.clean(i2)
    a.fdu.undefine(i1)
    a.fdu.undefine(i2)
    a.fdu.offload(e2_uuid)
    a.fdu.offload(e_uuid)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('[Usage] {} <yaks ip:port> <path to fdu descripto> <fdu 2>  <node id> <node2>' .format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
