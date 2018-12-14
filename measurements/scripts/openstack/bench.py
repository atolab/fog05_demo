import openstack
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


def read_binary_file(file_path):
    data = None
    with open(file_path, 'rb') as f:
        data = f.read()
    return data


def main(image_name, tries):
    conn = openstack.connect()

    flv_name = 'm1.fos'
    net_name = 'lan1'
    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor(flv_name)
    network = conn.network.find_network(net_name)

    dep_res = []
    for i in range(0, tries):
        print('Run {} started '.format(i+1))
        t_zero = time.time()

        server = conn.compute.create_server(
            name="bench", image_id=image.id, flavor_id=flavor.id,
            networks=[{"uuid": network.id}])

        server = conn.compute.wait_for_server(server)
        e_ip = server.access_ipv4
        flag = False
        while not flag:
            try:
                r = requests.get('http://{}'.format(e_ip), timeout=0.1)
                flag = True
            except:
                flag = False

        t_one = time.time()

        t_dep = t_one - t_zero

        conn.compute.delete_server(server, force=True)

        while conn.compute.find_server("bench", ignore_missing=True) is not None:
            pass

        dep_res.append(t_dep)
        print('Run {} took: {} '.format(i+1, t_dep))
        time.sleep(1)

    data = {
        'os_total_tries': tries,
        'os_deploy_times': dep_res
    }
    scipy.io.savemat('results-os-{}.mat'.format(tries), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[Usage] {} <image name> <tries>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], int(sys.argv[2]))
