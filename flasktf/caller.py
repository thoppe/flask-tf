import requests
import json
from serializers import pack, unpack

class baseCaller(object):

    def __init__(self):
        self.url = "http://127.0.0.1:5000/"

    def info(self, *args):
        url = self.url + 'info'
        r = requests.post(url, json=args)
        return json.loads(r.content)

class tfCaller(baseCaller):

    def __call__(self, *targets, **feed_dict):  # pragma: no cover
        url = self.url + 'tfcall'
        files = {'_targets': pack(targets)}
        for k, v in feed_dict.items():
            files[k] = pack(v)

        r = requests.post(url, files=files)
        if r.status_code != 200:
            raise ValueError(r.content)
        
        obj = unpack(r.content)

        # Cleanup the numpy cruft
        return obj.ravel()[0]


class kerasCaller(baseCaller):

    def __call__(self, *args):  # pragma: no cover
        
        url = self.url + 'kerascall'
        files = {}
        for k,x in enumerate(args):
            files["input{}".format(k)] = pack(x)

        r = requests.post(url, files=files)
        if r.status_code != 200:
            raise ValueError(r.content)

        print r
        exit()
        
        obj = unpack(r.content)

        print        

        print "DIE HERE"
        exit()
        
