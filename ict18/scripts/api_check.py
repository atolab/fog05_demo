import os
from meao_api import MEAO_API
import sys


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    a = MEAO_API(endpoint='192.168.1.129')
    desc = read(sys.argv[1])
    a.deploy_service(desc)
    input('Press enter to exit')
    a.close()


if __name__ == '__main__':
    main()
