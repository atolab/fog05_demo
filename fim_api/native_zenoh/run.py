import os
from fog05 import FIMAPI
import sys
import time
import json
import copy
import uuid

DESC_FOLDER = './'
descs = [
            ('fdu_zenoh_broker.json','0b5fe844-38ed-48e3-b927-bc4855f43682'), # six
            ('fdu_zenoh_sensors.json','64b067b6-abcc-41c5-b589-9c412bcd679b'), # un
            ('fdu_zenoh_subscriber.json','09aedb44-a89c-448a-adef-58d95e1085e9') # sept
        ]

# descs = [
#             ('test.json','0b5fe844-38ed-48e3-b927-bc4855f43682'), # six
#         ]

# descs = [
#             ('fdu_zenoh_broker.json','0b5fe844-38ed-48e3-b927-bc4855f43682'), # six
#         ]


def read(fname):
    return open(fname).read()


def main(ip):
    a = FIMAPI(locator=ip)

    nodes = a.node.list()
    print('Nodes: {}'.format(nodes))

    fdus = {}

    input('Press enter to instantiate the demo')



    for d in descs:
        df,n = d
        ds = json.loads(read(os.path.join(DESC_FOLDER,df)))
        fdu_id = a.fdu.onboard(ds)
        iid = a.fdu.instantiate(fdu_id, n)
        print('Instantiated: {}'.format(ds['name']))
        fdus.update({fdu_id: iid})
        time.sleep(1)

    input('Press enter to terminate the demo')

    for k in fdus:
        iid = fdus[k]
        a.fdu.terminate(iid)
        a.fdu.offload(k)

    print('Bye!')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage {} <ip>")
        exit -1
    main(sys.argv[1])
