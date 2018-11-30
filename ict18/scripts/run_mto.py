import os
import requests
import sys
import time
import json


HOST = '192.168.1.129'
PORT = 1919
PROTOCOL = 'http'
PREFIX = 'api'
API_VERSION = 'v0.1'
URL_PREFIX = '/{prefix}/{version}'.format(
    prefix=PREFIX,
    version=API_VERSION)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    print("Deploy MEC Service and Application using 5GCity MTO")
    main_url = "{0}://{1}:{2}".format(PROTOCOL, HOST, PORT)
    main_api_url = "{0}{1}".format(main_url,
                                   URL_PREFIX)
    headers = {"Content-type": "application/json"}
    data = {"name": "RNIS Demo Service",
            "descriptor-type": "meappdesc",
            "descriptor": read('rnis.json'),
            "slice-user": "Demo",
            "slice-id": "slice1"}
    response = requests.post("{0}/generic_service".
                             format(main_api_url),
                             headers=headers,
                             json=data)
    rnis_data = json.loads(response.text)
    print('RNIS Deployed id: {}'.format(rnis_data.get('_id').get('$oid')))
    time.sleep(5)
    data = {"name": "RNIS Dashboard",
            "descriptor-type": "meappdesc",
            "descriptor": read('view.json'),
            "slice-user": "Demo",
            "slice-id": "slice1"}
    response = requests.post("{0}/generic_service".
                             format(main_api_url),
                             headers=headers,
                             json=data)
    view_data = json.loads(response.text)
    print('Dashboard Deployed id: {}'.format(view_data.get('_id').get('$oid')))
    input("Press enter to remove")
    service_url = "{0}/generic_service/{1}".format(
        main_api_url,
        view_data["_id"]["$oid"])
    requests.delete(service_url)
    time.sleep(2)
    service_url = "{0}/generic_service/{1}".format(
        main_api_url,
        rnis_data["_id"]["$oid"])
    requests.delete(service_url)


if __name__ == '__main__':
    main()
