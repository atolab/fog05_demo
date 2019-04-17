from fog05 import FIMAPI
import uuid
import json
import sys
import os


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, fdufile, n1):
    a = FIMAPI(ip)

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {}'.format(n))

    fdu_d = json.loads(read_file(fdufile))

    e_uuid = fdu_d.get('uuid')

    #n1 = '90c02ec42f2a47448d5f8e33ad7bf7e2'
    #n2 = '297b270c79eb45089b6979f86fbdaa96'
    #n1 = '21e48018-d4c3-499e-baee-6990e33a6c0c'

    input('press enter to onboard descriptor')
    a.fdu.onboard(fdu_d)
    input('Press enter to define')
    iid = a.fdu.define(e_uuid, n1)
    #a.entity.define(e_manifest, n2, wait=True)
    input('Press enter to configure')
    a.fdu.configure(iid)
    input('Press enter to run')
    a.fdu.start(iid)

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

    a.fdu.stop(iid)
    a.fdu.clean(iid)
    a.fdu.undefine(iid)
    a.fdu.offload(e_uuid)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[Usage] {} <yaks ip:port> <path to fdu descripto> <node id>' .format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
