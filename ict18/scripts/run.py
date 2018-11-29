import os
from meao_api import MEAO_API
import sys
import time


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    a = MEAO_API(endpoint='192.168.1.129')
    desc = read("rnis.json")
    a.deploy_service(desc)
    time.sleep(5)
    desc = read("view.json")
    a.deploy_service(desc)
    a.close()


if __name__ == '__main__':
    main()
