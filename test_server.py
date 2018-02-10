from flasktf import caller
import numpy as np


M = caller()
terms = M.info()
print M.info(*terms)

N = 100
x = np.random.uniform(size=(N,))
y = np.random.uniform(size=(N,))
print M('z', x=x, y=y)

