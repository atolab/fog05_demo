from fog05 import FAEMAPI
from fog05.interfaces.AtomicEntity import AtomicEntity
import uuid
import json
import sys
import os
import code

def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, ae_file):
    a = FAEMAPI(ip)

    ae_d = AtomicEntity(json.loads(read_file(ae_file)))


    input('press enter to onboard descriptor')
    res = a.atomic_entity.onboard(ae_d)
    print(res)
    e_uuid = res.get_uuid()
    # code.interact(local=locals())



    input('Press enter to instantiate')
    inst_info = a.atomic_entity.instantiate(e_uuid)
    print(inst_info)
    instid = inst_info.get_uuid()

    input('Press enter to remove')

    a.atomic_entity.terminate(instid)
    a.atomic_entity.offload(e_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[Usage] {} <yaks ip:port> <path to fdu descriptor>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2])
