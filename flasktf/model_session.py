'''
When passed a model def., caller creates an object that can be called
easily. In the future, this will validate input (rank at least!).
'''

import pylru
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class baseModelSession(object):

    def __init__(self, model_func=None, *args, **kwargs):
        self.sess = None

        if model_func is not None:
            self.set_model(model_func, *args, **kwargs)

    def configTF(self):
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.InteractiveSession(config=config)

    def _check_model_set(self):
        if self.sess is None:
            raise ValueError("set_model has not been run")

    def get_variables(self):
        self._check_model_set()
        return self.var

    def __getitem__(self, key):
        try:
            return self.var[key]
        except KeyError:
            msg = "{} is not defined in the model"
            raise KeyError(msg.format(key))

    @pylru.lrudecorator(128)
    def get_info(self, name):
        x = self[name]
        val = {
            "rank": x.get_shape().ndims,
            "dtype": str(x.dtype),
        }
        if not val['rank']:
            val['rank'] = 0
        return val


class tfModelSession(baseModelSession):

    def set_model(self, model_func):
        self.configTF()

        self.var = model_func()
        if not self.var:
            raise ValueError("No variables returned by model function.")

        self.sess.run(tf.global_variables_initializer())

    def __call__(self, *targets, **feed_args):
        self._check_model_set()

        feed_dict = {self[k]: v for k, v in feed_args.items()}
        target_vars = [self[k] for k in targets]

        try:
            result = self.sess.run(target_vars, feed_dict=feed_dict)
        except tf.errors.InvalidArgumentError as Ex:
            raise(Ex)

        return dict(zip(targets, result))
