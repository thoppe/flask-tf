import tensorflow as tf
from tfFlask import tfFlask

def simple_add():
    x = tf.placeholder(tf.float32, name='x')
    y = tf.placeholder(tf.float32, name='y')
    z = tf.add(x, y, name='z')

tfFlask.register(simple_add)
tfFlask.run()
