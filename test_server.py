from tfFlask.tfFlask import tfFlask
import numpy as np
from tqdm import tqdm

M = tfFlask()

N = 100
x = np.random.uniform(size=(N,))
y = np.random.uniform(size=(N,))
print M.serve('z',x=x,y=y)
print x.dot(y)
