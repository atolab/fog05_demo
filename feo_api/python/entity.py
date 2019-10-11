from fog05 import FAEMAPI
from fog05 import FEOAPI
from fog05.interfaces.AtomicEntity import AtomicEntity
from fog05.interfaces.Entity import Entity
import uuid
import json
import sys
import os
import code

def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, ae_file, e_file):
    a = FAEMAPI(ip)
    feo = FEOAPI(ip)

    ae_d = AtomicEntity(json.loads(read_file(ae_file)))
    e_d = Entity(json.loads(read_file(e_file)))


    input('press enter to onboard descriptors')
    ae_desc = a.atomic_entity.onboard(ae_d)
    print(ae_desc)
    ae_uuid = ae_desc.get_uuid()

    e_desc = feo.entity.onboard(e_d)
    print(e_desc)
    e_uuid = e_desc.get_uuid()
    # code.interact(local=locals())



    input('Press enter to instantiate')
    inst_info = feo.entity.instantiate(e_uuid)
    print(inst_info)
    instid = inst_info.get_uuid()

    input('Press enter to remove')

    feo.entity.terminate(instid)
    feo.entity.offload(e_uuid)
    a.atomic_entity.offload(ae_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[Usage] {} <yaks ip:port> <path to atomic entity> <path to entity>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
