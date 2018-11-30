import os
from meao_api import MEAO_API
import sys
import time
import json


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    a = MEAO_API(endpoint='192.168.1.129')
    desc = read("rnis.json")
    a.deploy_service(desc)
    d1 = json.loads(desc)
    time.sleep(5)
    desc = read("view.json")
    d2 = json.loads(desc)
    a.deploy_service(desc)
    input("press enter to remove")
    a.remove_service(d1.get('appd-descriptor').get('id'))
    time.sleep(5)
    a.remove_service(d2.get('appd-descriptor').get('id'))
    #nput("press enter to exit")
    # a.close()


if __name__ == '__main__':
    main()
