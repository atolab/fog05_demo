from fog05 import FIMAPI
import uuid
import json
import sys
import os


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, fdufile, netfile):
    a = FIMAPI(ip)

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {}'.format(n))

    fdu_d = json.loads(read_file(fdufile))
    net_d = json.loads(read_file(netfile))

    e_uuid = fdu_d.get('uuid')
    n_uuid = net_d.get('uuid')

    input("Press enter to create network")
    a.network.add_network(net_d)

    #n1 = '90c02ec42f2a47448d5f8e33ad7bf7e2'
    #n2 = '297b270c79eb45089b6979f86fbdaa96'
    #n1 = '16892ae12009411ab76998fdb7ccaf91'
    n1 = 'e0e442af51d14802a9bc71b5e634440e'
    #n1 = 'a2d358aaaf2b42cb8d23a89e88b97e5c'

    input('press enter to onboard descriptor')
    a.fdu.onboard(fdu_d)
    input('Press enter to define')
    intsid = a.fdu.define(e_uuid, n1)
    input('Press enter to configure')
    a.fdu.configure(intsid)
    input('Press enter to run')
    a.fdu.start(intsid)

    # input('Press enter to stop')
    # a.entity.stop(e_uuid, n1, i_uuid)
    # input('Press enter to clean')
    # a.entity.clean(e_uuid, n1, i_uuid)
    # input('Press enter to undefine')
    # a.entity.undefine(e_uuid, n1)

    # input('Press enter to migrate')

    #res = a.entity.migrate(e_uuid, i_uuid, n1, n2)
    #print('Res is: {}'.format(res))
    input('Press enter to remove')

    a.fdu.stop(intsid)
    a.fdu.clean(intsid)
    a.fdu.undefine(intsid)
    a.fdu.offload(e_uuid)
    input("Press enter to remove network")
    a.network.remove_network(n_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[Usage] {} <yaks ip:port> <path to fdu descripto> <path to net descriptor>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3])