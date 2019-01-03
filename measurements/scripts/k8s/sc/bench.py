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


def create_deployment_object(name, ports=False):
    # Configureate Pod template container
    if ports:
        container = client.V1Container(
            name="name",
            image="nginx:1.7.9",
            ports=[client.V1ContainerPort(container_port=80)])
    else:
        container = client.V1Container(
            name="name",
            image="nginx:1.7.9")
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=1,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)

    return deployment


def main(tries, chain_length):

    token = time.time()
    dep_res = []
    deployments = []

    for index in range(0, tries):
        print('Run {} started '.format(index+1))
        config.load_kube_config()
        k8s_client = client.ApiClient()
        v1 = client.CoreV1Api()
        api = client.ExtensionsV1beta1Api()
        t_zero = time.time()
        os.system("cat nginx.tar.gz | sudo docker image load")
        for i in range(0, chain_length):
            name = 'item{}'.format(i)
            if i == (chain_length-1):
                dep = create_deployment_object(name, ports=True)
            else:
                dep = create_deployment_object(name)
            api_response = api.create_namespaced_deployment(
                body=dep,
                namespace="default")
            deployments.append((name, dep))

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

        for n, _ in deployments:
            api.delete_namespaced_deployment(
                name=n,
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
    if len(sys.argv) < 3:
        print('[Usage] {} <tries> <chain length>'.format(
            sys.argv[0]))
        exit(0)
    main(int(sys.argv[1]), int(sys.argv[2]))