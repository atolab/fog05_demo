import os
from fog05 import FIMAPI
import sys
import time
import json


DESC_FOLDER = '../descriptors'
net_desc = ['vnet_mec.json']
descs = ['mecp.json','gw.json','mqtt.json','ap.json','rnis.json','webui.json']


def read(fname):
    return open(fname).read()


def main(nodeid):
    a = FIMAPI()

    fdus = {}
    nets = []

    input('Press enter to instantiate the demo')

    for d in net_desc:
        path_d = os.path.join(DESC_FOLDER,d)
        netd = read(path_d)
        a.network.add_network(netd)
        nets.append(netd['uuid'])
        time.sleep(1)

    for d in descs:
        path_d = os.path.join(DESC_FOLDER,d)
        fdu_d = read(path_d)
        fdu_id = a.fdu.onboard(fdu_d)
        iid = a.fdu.instantiate(fdu_id, nodeid)
        fdus.update({fdu_id: iid})
        time.sleep(1)

    input('Press enter to terminate the demo')

    for k in fdus:
        iid = fdus[k]
        a.fdu.terminate(iid)
        a.fdu.offload(k)

    for n in nets:
        a.network.remove_network(n)

    print('Bye!')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage {} <node id>")
        exit -1
    main(sys.argv[1])
