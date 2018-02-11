import tensorflow as tf
from flasktf import serve


def L2norm():
    x = tf.placeholder(tf.float32, shape=(None,))
    return {'x': x, 'z': tf.norm(x)}

serve(L2norm, debug=False)
