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


    n1 = 'a2d358aa-af2b-42cb-8d23-a89e88b97e5c' #fosmed
    #n1 = 'a4589fae-0493-40cf-b976-2d03020d060d' #foskvm
    n1 = '53712df2-9649-4a21-be2e-80eed00ff9ce' #ubuntuvm1
    n1 = 'de8c2f1c-9414-48ec-8400-a324cb1e6612' #ubuntuvm2
    n1 = 'd07b095f-7948-4f9b-95cc-c61029f6c3c3' #fosdbg

    input('press enter to onboard descriptor')
    a.fdu.onboard(fdu_d)
    input('Press enter to define')
    intsid = a.fdu.instantiate(e_uuid, n1)


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

    a.fdu.terminate(intsid)
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
