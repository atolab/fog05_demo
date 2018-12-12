from fog05 import API
import uuid
import json
import sys
import os
import time
import statistics
import scipy.io
import requests


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(entity_path, tries, nid, e_ip, y_ip):
    a = API(endpoint=y_ip)

    token = time.time()
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

    dep_res = []
    for i in range(0, tries):
        print('Run {} started '.format(i+1))
        t_zero = time.time()

        a.onboard(e_manifest)
        flag = False
        while not flag:
            try:
                r = requests.get('http://{}'.format(e_ip), timeout=0.01)
                flag = True
            except Exception as e:
                flag = False

        t_one_run = time.time()

        a.remove(e_manifest.get('uuid'))

        t_dep = t_one_run - t_zero

        dep_res.append(t_dep)
        print('Run {} took: {} '.format(i+1, t_dep))
        time.sleep(10)
    data = {
        'fos_total_tries': tries,
        'fos_deploy_times': dep_res
    }
    scipy.io.savemat('results-fos-{}.mat'.format(token), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('[Usage] {} <path to entity manifest> <tries> <nodeid> <ip of the machine> <ip of yaks>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
