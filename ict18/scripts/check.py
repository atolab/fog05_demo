from mec_im import appd
import json
from pyangbind.lib.serialise import pybindJSONDecoder
from collections import OrderedDict
from fog05.store import Store
from yaks import YAKS
import time


def obs(uri, value, v):
    print('5GCity MEAO Plugin - ME App Deploy Received')
    value = json.loads(value,  object_pairs_hook=OrderedDict)
    print('Value: {}'.format(value))
    uuid = uri.split('/')[-1]
    myappd = appd.appd()
    pybindJSONDecoder.load_ietf_json(value, None, None, obj=myappd)
    uri = '//afos/meao/mecapp/{}'.format(uuid)

def main():
    yapi = YAKS('192.168.86.44')
    dstore = Store(yapi, '//dfos/', "meao", 1024)
    uri = '//dfos/meao/mecapp/**'
    dstore.observe(uri, obs)
    while True:
        time.sleep(1000)


if __name__ == '__main__':
    main()
