import requests	
import json
from serializers import pack, unpack
	
#################################################################	
	
class caller(object):	
    def __init__(self):	
        self.url = "http://127.0.0.1:5000/"	
	
    def info(self, *args):	
        url = self.url + 'info'	
        r = requests.post(url, json=args)	
        return json.loads(r.content)	
	
    def __call__(self, *targets, **feed_dict):	
        url = self.url + 'serve'	
        files = {'_targets':pack(targets)}	
        for k,v in feed_dict.items():	
            files[k] = pack(v)	
            	
        r = requests.post(url, files=files)	
        return unpack(r.content)	
