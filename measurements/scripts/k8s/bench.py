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
    config.load_kube_config()
    k8s_client = client.ApiClient()
    k8s_api = utils.create_from_yaml(k8s_client, yaml_path)
    v1 = client.CoreV1Api()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()

    token = time.time()

    dep_res = []
    for i in range(0, tries):

        t_zero = time.time()
        deps = k8s_api.read_namespaced_deployment(
            name, "default")
        i = v1.list_namespaced_pod("default").items[0]
        ip = i.status.pod_ip
        flag = False
        while not flag:
            try:
                r = requests.get('http://{}'.format(e_ip))
                flag = True
            except:
                flag = False
        t_one = time.time()

        t_dep = t_one - t_zero

        extensions_v1beta1.delete_namespaced_deployment(
            name=name,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground')
        os.system("sudo docker image rm 84581e99d807")
        dep_res.append(t_dep)
        print('Run {}'.format(i+1))
        time.sleep(5)

    data={
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
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
