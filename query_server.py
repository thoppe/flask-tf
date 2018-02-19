import keras
from flasktf import tfCaller, kerasCaller
import numpy as np

#model = tfCaller()
#print model('z', x=[1,2,3], y=[0,1,2])
# Returns {"z": 8.0}
#exit()

model = kerasCaller()
x = np.array(np.linspace(0, 1, 3),).reshape(1, -1)
print model(x).content


