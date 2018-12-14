from pylxd import Client
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


def main(image_path, tries, e_ip):
    net_conf = '{"name":"eth0","type":"nic","parent":"virbr0","nictype":"bridged","hwaddr":"52:54:00:b8:c2:ba"}'
    client = Client()
    image_data = read_binary_file(image_path)

    alias = 'bench'

    dep_res = []
    for i in range(0, tries):
        print('Run {} started '.format(i+1))
        t_zero = time.time()

        img = client.images.create(image_data, public=True, wait=True)
        img.add_alias(alias, description="Bench image")
        profile = client.profiles.create(alias)
        profile.devices = net_conf
        profile.save()

        cont_conf = {'name': alias, 'profiles': alias,
                     'source': {'type': 'image', 'alias': alias}}

        container = client.containers.create(cont_conf, wait=True)
        container.start()
        flag = False
        while not flag:
            try:
                r = requests.get('http://{}'.format(e_ip), timeout=0.1)
                flag = True
            except:
                flag = False

        t_one = time.time()

        t_dep = t_one - t_zero

        container.stop(force=False, wait=True)
        while container.status != 'Stopped':
            container.sync()
        container.delete()
        while True:
            if len(profile.used_by) == 0:
                break
            time.sleep(1)
        profile.delete()
        img.delete()

        dep_res.append(t_dep)
        print('Run {} took: {} '.format(i+1, t_dep))
        time.sleep(1)

    data = {
        'lxd_total_tries': tries,
        'lxd_deploy_times': dep_res
    }
    scipy.io.savemat('results-lxd-{}.mat'.format(tries), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[Usage] {} <path to lxd image> <tries> <ip of the machine>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
