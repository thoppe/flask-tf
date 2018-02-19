from nose.tools import raises
from nose.tools import assert_equal

from flasktf.model_session import tfModelSession, kerasModelSession
import numpy as np
import tensorflow as tf

import keras.models
import keras.layers


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

    def keras_softmax_test(self):

        def model(N):
            x = keras.layers.Input(shape=(N,),)
            y = keras.layers.Activation(activation='softmax')(x)
            model = keras.models.Model(inputs=x, outputs=y)
            return model

        T = kerasModelSession(model, N=5)
        x = np.array(np.linspace(0, 1, 5),).reshape(1, -1)
        yx = T(x)
        yp = np.exp(x) / np.exp(x).sum()

        np.testing.assert_array_almost_equal(yx, yp)

    def rank_test(self):
        def model():
            x0 = tf.placeholder(tf.float32)
            x1 = tf.placeholder(tf.float32, shape=(None,))
            x2 = tf.placeholder(tf.float32, shape=(None, 10))
            return {'x0': x0, 'x1': x1, 'x2': x2}

        T = tfModelSession(model)
        assert_equal(T.get_info('x0')['rank'], 0)
        assert_equal(T.get_info('x1')['rank'], 1)
        assert_equal(T.get_info('x2')['rank'], 2)

    @raises(ValueError)
    def no_vars_in_model_test(self):

        def model():
            pass

        T = tfModelSession(model)
        T.get_variables()

    @raises(ValueError)
    def no_model_set_get_var_test(self):
        T = tfModelSession()
        T.get_variables()

    @raises(ValueError)
    def no_model_set_tf_call_test(self):
        T = tfModelSession()
        T('z')

    @raises(ValueError)
    def no_model_set_keras_call_test(self):
        T = kerasModelSession()
        T('z')

    @raises(KeyError)
    def missing_var_in_index_test(self):

        def model():
            x = tf.placeholder(tf.float32, shape=(None,))
            return {'x': x, 'z': tf.norm(x)}

        # There is no variable named q in the model
        T = tfModelSession(model)
        T['q']

    @raises(KeyError)
    def missing_var_in_call_test(self):

        def model():
            x = tf.placeholder(tf.float32, shape=(None,))
            return {'x': x, 'z': tf.norm(x)}

        # There is no variable named q in the model
        T = tfModelSession(model)
        T('q', x=[1, 2, 3])

    @raises(tf.errors.InvalidArgumentError)
    def not_enough_info_to_solve_test(self):

        def model():
            x = tf.placeholder(tf.float32, shape=(None,))
            return {'x': x, 'z': tf.norm(x)}

        # Model requires 'x'
        T = tfModelSession(model)
        T('z')
