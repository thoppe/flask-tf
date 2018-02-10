import tensorflow as tf
from tfFlask import serve

def scalar_add():
    x = tf.placeholder(tf.float32)
    y = tf.placeholder(tf.float32)
    z = tf.add(x, y)
    return {'x':x, 'y':y, 'z':z}

def L2norm():
    x = tf.placeholder(tf.float32, shape=(None,))
    return {'x':x, 'z':tf.norm(x)}

def dot_product():
    x = tf.placeholder(tf.float32, shape=(None,),name='x')
    y = tf.placeholder(tf.float32, shape=(None,),name='y')
    return {'x':x, 'y':y, 'z':tf.tensordot(x,y,1)}


serve(dot_product)
