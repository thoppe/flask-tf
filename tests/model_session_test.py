from flasktf.model_session import tfModelSession

import numpy as np
import tensorflow as tf


class Serializer_Test:

    @classmethod
    def setup_class(cls):
        pass

    def scalar_add_test(self):

        def model():
            x = tf.placeholder(tf.float32)
            y = tf.placeholder(tf.float32)
            z = tf.add(x, y)
            return {'x': x, 'y': y, 'z': z}

        T = tfModelSession(model)

        x, y = 2, 3

        result = T('z', x=x, y=y)['z']
        np.testing.assert_equal(result, x + y)

    def vector_add_test(self):

        def model():
            x = tf.placeholder(tf.float32, shape=(None,))
            y = tf.placeholder(tf.float32, shape=(None,))
            z = tf.add(x, y, name='z')
            return {'x': x, 'y': y, 'z': z}

        T = tfModelSession(model)
        x = np.random.uniform(size=(10,))
        y = np.random.uniform(size=(10,))

        result = T('z', x=x, y=y)['z']
        np.testing.assert_array_almost_equal(result, x + y)

    def l2norm_test(self):

        def model():
            x = tf.placeholder(tf.float32, shape=(None,))
            return {'x': x, 'z': tf.norm(x)}

        T = tfModelSession(model)
        x = np.linspace(0, 1, 5)

        result = T('z', x=x)['z']
        np.testing.assert_array_almost_equal(
            result,
            np.linalg.norm(x)
        )
