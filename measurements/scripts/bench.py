from fog05 import API
import uuid
import json
import sys
import os
from time import time
import statistics
import scipy.io
import requests


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(entity_path, tries, nid, e_ip, y_ip):
    a = API(endpoint=y_ip)

    token = time()
    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    ns = []
    for i, _ in nodes:
        ns.append(i)

    if nid not in ns:
        print('Selected node is not available!!')
        exit(-1)

    e_manifest = json.loads(read_file(entity_path))

    e_uuid = e_manifest.get('uuid')
    i_uuid = '{}'.format(uuid.uuid4())

    conf_res = []
    run_res = []
    dep_res = []
    for i in range(0, tries):

        t_zero = time()

        a.entity.define(e_manifest, nid, wait=True)

        t_zero_conf = time()
        a.entity.configure(e_uuid, nid, i_uuid, wait=True)
        t_one_conf = time()

        t_zero_run = time()
        a.entity.run(e_uuid, nid, i_uuid, wait=True)
        flag = False
        while flag:
            try:
                r = requests.get('http://{}'.format(e_ip))
            except:
                flag = False

        t_one_run = time()

        t_conf = t_one_conf - t_zero_conf
        t_run = t_one_run - t_zero_run
        t_dep = t_one_run - t_one

        a.entity.stop(e_uuid, nid, i_uuid, wait=True)
        a.entity.clean(e_uuid, nid, i_uuid, wait=True)
        a.entity.undefine(e_uuid, nid, wait=True)

        conf_res.append(t_conf)
        run_res.append(t_run)
        dep_res.append(t_dep)

    data = {
        'total_tries': tries,
        'configuration_times': conf_res,
        'run_times': run_res,
        'deploy_times': dep_res
    }
    scipy.io.savemat('results-{}.mat'.format(token), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('[Usage] {} <path to entity manifest> <tries> <nodeid> <ip of the machine> <ip of yaks>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
