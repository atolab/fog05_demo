from fog05rest import FIMAPI
import uuid
import json
import sys
import os


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, fdufile, netfile, img_file, img_data):
    a = FIMAPI(ip)


    fdu_d = json.loads(read_file(fdufile))
    net_d = json.loads(read_file(netfile))
    img_d = json.loads(read_file(img_file))


    e_uuid = fdu_d.get('uuid')
    n_uuid = net_d.get('uuid')

    raw_input("Press enter to create image")
    a.image.add(img_d, img_data)

    raw_input("Press enter to create network")
    a.network.add_network(net_d)

    #n1 = '90c02ec42f2a47448d5f8e33ad7bf7e2'
    #n2 = '297b270c79eb45089b6979f86fbdaa96'
    n1 = 'e0e442af51d14802a9bc71b5e634440e'

    raw_input('press enter to onboard descriptor')
    a.fdu.onboard(fdu_d)
    raw_input('Press enter to instantiate')
    instid = a.fdu.instantiate(e_uuid, n1)
    print('Instance ID %s' % instid)

    raw_input('Press enter to remove')

    a.fdu.terminate(instid)
    a.fdu.offload(e_uuid)
    raw_input("Press enter to remove network")
    a.network.remove_network(n_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('[Usage] {} <rest server ip> <path to fdu descripto> <path to net descriptor> <path to image descriptor> <path to image file>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
