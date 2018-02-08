import requests
import numpy as np

url = "http://127.0.0.1:5000/"
r = requests.get(url)
print r.content



url = "http://127.0.0.1:5000/check"
args = ['x','z']
r = requests.post(url, json=args)
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
