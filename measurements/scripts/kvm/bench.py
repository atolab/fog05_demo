import libvirt
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


def main(xml_path, tries, e_ip):
    a = libvirt.open('qemu:///system')

    token = time.time()

    dep_res = []
    for i in range(0, tries):
        print('Run {} started '.format(i+1))
        t_zero = time.time()
        dom = a.defineXML(read_file(xml_path))
        dom.create()
        flag = False
        while not flag:
            try:
                r = requests.get('http://{}'.format(e_ip), timeout=0.1)
                flag = True
            except:
                flag = False
        t_one = time.time()

        t_dep = t_one - t_zero

        dom.destroy()
        while dom.isActive():
            pass
        dom.undefine()
        dep_res.append(t_dep)
        print('Run {} took: {} '.format(i+1, t_dep))
        time.sleep(1)

    data = {
        'kvm_total_tries': tries,
        'kvm_deploy_times': dep_res
    }
    scipy.io.savemat('results-hv-{}.mat'.format(token), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[Usage] {} <path to vm xml> <tries> <ip of the machine>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
