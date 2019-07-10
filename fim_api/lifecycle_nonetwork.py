from fog05 import FIMAPI
import uuid
import json
import sys
import os


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, fdufile):
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


    n1 = 'a2d358aa-af2b-42cb-8d23-a89e88b97e5c' #fos med


    input('press enter to onboard descriptor')
    a.fdu.onboard(fdu_d)
    input('Press enter to instantiate')
    intsid = a.fdu.instantiate(e_uuid, n1)

    input('Press enter to remove')

    a.fdu.terminate(intsid)
    a.fdu.offload(e_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[Usage] {} <yaks ip:port> <path to fdu descriptor>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2])
