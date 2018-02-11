import tensorflow as tf
from flasktf import serve

def dot_product():
    x = tf.placeholder(tf.float32, shape=(None,),name='x')
    y = tf.placeholder(tf.float32, shape=(None,),name='y')
    return {'x':x, 'y':y, 'z':tf.tensordot(x,y,1)}

serve(dot_product)
