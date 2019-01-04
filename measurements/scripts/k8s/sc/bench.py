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


def create_deployment_object(name, port):
    # Configureate Pod template container

    container = client.V1Container(
        name=name,
        image="nginx:1.7.9",
        ports=[client.V1ContainerPort(container_port=port)])
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
        os.system("cat ../nginx.tar.gz | sudo docker image load")
        for i in range(0, chain_length):
            name = 'item{}'.format(i)
            if i == (chain_length-1):
                dep = create_deployment_object(name, 80)
            else:
                if i < 10:
                    p = int('808{}'.format(i))
                else:
                    p = int('80{}'.format(i))
                dep = create_deployment_object(name, p)
            api_response = api.create_namespaced_deployment(
                body=dep,
                namespace="default")
            pods = v1.list_namespaced_pod("default").items
            while len(pods) != i+1:
                pods = v1.list_namespaced_pod("default").items
            pod = [x for x in pods if name in x.metadata.name][0]
            while len(pod.spec.containers) == 0:
                pods = v1.list_namespaced_pod("default").items
                pod = [x for x in pods if name in x.metadata.name][0]
            cont = [x for x in pods if x.spec.containers[0].name == name][0]
            while cont.status.pod_ip is None:
                pods = v1.list_namespaced_pod("default").items
                cont = [x for x in pods if x.spec.containers[0].name == name][0]
            ip = cont.status.pod_ip
            print('IP is {}:{}'.format(ip, p))
            if i < (chain_length-1):
                flag = False
                while not flag:
                    try:
                        r = requests.get(
                            'http://{}:{}'.format(ip, p), timeout=0.1)
                        flag = True
                    except:
                        flag = False
            deployments.append((name, dep))

        pods = v1.list_namespaced_pod("default").items
        while len(pods) < chain_length:
            pods = v1.list_namespaced_pod("default").items
        cont = [x for x in pods if x.spec.containers[0].name == name][0]
        ip = cont.status.pod_ip
        while ip is None:
            pods = v1.list_namespaced_pod("default").items
            cont = [x for x in pods if x.spec.containers[0].name == name][0]
            ip = cont.status.pod_ip
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

        i = v1.list_namespaced_pod("default").items
        while len(i) != 0:
            i = v1.list_namespaced_pod("default").items

        os.system("sudo docker image rm 84581e99d807")

        dep_res.append(t_dep)
        print('Run {} took: {} '.format(index+1, t_dep))

    data = {
        'k8s_deploy_times': dep_res
    }
    scipy.io.savemat('results-k8s-{}-{}.mat'.format(chain_length, tries), data)
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[Usage] {} <tries> <chain length>'.format(
            sys.argv[0]))
        exit(0)
    main(int(sys.argv[1]), int(sys.argv[2]))
