import tensorflow as tf
from tfFlask import tfFlask

'''
def simple_add():
    x = tf.placeholder(tf.float32, name='x')
    y = tf.placeholder(tf.float32, name='y')
    z = tf.add(x, y, name='z')

tfFlask.register(simple_add)
tfFlask.run()
'''

def L2norm():
    x = tf.placeholder(tf.float32, shape=(None,), name='x')
    z = tf.norm(x, name='z')

tfFlask.register(L2norm)
tfFlask.run()
