import sys
import os
import time
import statistics
import scipy.io
import requests
import docker


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(tries, chain_length):

    token = time.time()
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    dep_res = []
    for index in range(0, tries):
        print('Run {} started '.format(index+1))
        t_zero = time.time()
        os.system("cat nginx.tar.gz | docker image load")
        conts = []
        #imgid = client.import_image_from_file('nginx.tar.gz')
        for i in range(0, chain_length):
            if i == (chain_length-1):
                hc = client.create_host_config(port_bindings={80: 80})
                cid = client.create_container(
                    'nginx:1.7.9', ports=[80],
                    host_config=hc, name='bench{}'.format(i))
            else:
                cid = client.create_container(
                    'nginx:1.7.9', name='bench{}'.format(i))
            client.start(cid)
            conts.append(cid)
        flag = False
        while not flag:
            try:
                r = requests.get(
                    'http://{}'.format('127.0.0.1'), timeout=0.1)
                flag = True
            except:
                flag = False
        t_one = time.time()

        t_dep = t_one - t_zero

        for cid in conts:
            client.kill(cid)
            client.remove_container(cid)
        client.remove_image('nginx:1.7.9')
        #os.system("docker image rm 84581e99d807")
        dep_res.append(t_dep)
        print('Run {} took: {} '.format(index+1, t_dep))
        time.sleep(1)

    data = {
        'docker_deploy_times': dep_res
    }
    scipy.io.savemat('results-hv-{}.mat'.format(token), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[Usage] {} <tries> <chain_length>'.format(
            sys.argv[0]))
        exit(0)
    main(int(sys.argv[1]), int(sys.argv[2]))
