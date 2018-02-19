import tensorflow as tf
import keras.layers, keras.models
from flasktf import serveTF, serveKeras

'''
def dot_product():
    x = tf.placeholder(tf.float32, shape=(None,),name='x')
    y = tf.placeholder(tf.float32, shape=(None,),name='y')
    return {'x':x, 'y':y, 'z':tf.tensordot(x,y,1)}

serveTF(dot_product)
'''


def softmax(N):
    x = keras.layers.Input(shape=(N,),)
    y = keras.layers.Activation(activation='softmax')(x)
    return keras.models.Model(inputs=x, outputs=y)

serveKeras(softmax, N=3)
