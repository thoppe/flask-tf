import requests
import StringIO
import json
import numpy as np

url = "http://127.0.0.1:5000/"
r = requests.get(url)
print r.content


url = "http://127.0.0.1:5000/check"
args = ['x','z']
r = requests.post(url, json=args)
print r.content

A = np.array([1.0,2.0,3])# any NumPy array
memfile = StringIO.StringIO()
np.save(memfile, A)
memfile.seek(0)
serialized = memfile.read()#.decode('latin-1'))


## Need to figure out how to pass vars AND target
url = "http://127.0.0.1:5000/serve"
targets = ['z']
r = requests.post(url, files={'x':serialized, 'y':serialized,
                              'json':(None,json.dumps(targets))})
print r.content


exit()



'''
for n in range(20):
    args = {"x":n, "y":n**2, "target":"z"}
    r = requests.post(url, json=args)
    print r.content
'''

#args = {"x":np.linspace(0,1,10,np.float64),"target":"z"}
#args = {"x":np.linspace(0,20,10,np.int32),"target":"z"}
#args  ={"x":np.linspace(0,20,10,np.int32),"target":"z"}
args = {"target":"z"}
x = np.linspace(0,20,10,np.float64)
args['x'] = x.tostring()

#print x
#print np.fromstring(x,dtype=args['x'].dtype)
#print np.fromstring(x)
#exit()

r = requests.post(url, json=args)
print r.content
