'''
When passed a model def., caller creates an object that can be called
easily. In the future, this will validate input (rank at least!).
'''

import pylru
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class tfModelSession(object):

    def __init__(self, model_func=None):
        if model_func is not None:
            self.set_model(model_func)

    def set_model(self, model_func):
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.InteractiveSession(config=config)
        self.g = tf.get_default_graph()

        self.var = model_func()
        if not self.var:
            raise Warning("No variables returned by model function.")

        self.sess.run(tf.global_variables_initializer())

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

    def __call__(self, *targets, **feed_args):
        feed_dict = {self[k]: v for k, v in feed_args.items()}
        target_vars = [self[k] for k in targets]

        result = self.sess.run(target_vars, feed_dict=feed_dict)
        return dict(zip(targets, result))
