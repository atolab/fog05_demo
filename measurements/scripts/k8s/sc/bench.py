import sys
import os
import time
import statistics
import scipy.io
import requests
from kubernetes import client, config, utils


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(yaml_path, name, tries):

    token = time.time()

    dep_res = []
    for index in range(0, tries):
        print('Run {} started '.format(index+1))
        config.load_kube_config()
        k8s_client = client.ApiClient()
        k8s_api = utils.create_from_yaml(k8s_client, yaml_path)
        v1 = client.CoreV1Api()
        extensions_v1beta1 = client.ExtensionsV1beta1Api()
        t_zero = time.time()
        os.system("cat nginx.tar.gz | sudo docker image load")
        deps = k8s_api.read_namespaced_deployment(
            name, "default")
        i = v1.list_namespaced_pod("default").items
        while len(i) == 0:
            i = v1.list_namespaced_pod("default").items
        ip = i[0].status.pod_ip
        while ip is None:
            i = v1.list_namespaced_pod("default").items
            ip = i[0].status.pod_ip
        print('IP is {}'.format(ip))
        flag = False
        while not flag:
            try:
                r = requests.get('http://{}'.format(ip), timeout=0.1)
                flag = True
            except:
                flag = False
        t_one = time.time()

        t_dep = t_one - t_zero

        extensions_v1beta1.delete_namespaced_deployment(
            name=name,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground'))

        time.sleep(10)

        os.system("sudo docker image rm 84581e99d807")

        dep_res.append(t_dep)
        print('Run {} took: {} '.format(index+1, t_dep))
        time.sleep(5)

    data = {
        'k8s_total_tries': tries,
        'k8s_deploy_times': dep_res
    }
    scipy.io.savemat('results-hv-{}.mat'.format(token), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[Usage] {} <path to k8s yaml> <deployment name> <tries>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
