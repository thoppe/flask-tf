import pylru
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class tfModel(object):

    def __init__(self, model_func):
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
        return {
            "name":name,
            "rank":x.get_shape().ndims,
            "dtype":x.dtype,
        }
        

    def __call__(self, *targets, **feed_args):
        feed_dict = {self[k]:v for k,v in feed_args.items()}
        target_vars = [self[k] for k in targets]

        result = self.sess.run(target_vars, feed_dict=feed_dict)
        return dict(zip(targets, result))
        
if __name__ == "__main__":

    def scalar_add():
        x = tf.placeholder(tf.float32)
        y = tf.placeholder(tf.float32)
        z = tf.add(x, y)
        return {'x':x, 'y':y, 'z':z}

    def vector_add():
        x = tf.placeholder(tf.float32, shape=(None,))
        y = tf.placeholder(tf.float32, shape=(None,))
        z = tf.add(x,y,name='z')
        return {'x':x, 'y':y, 'z':z}

    def L2norm():
        x = tf.placeholder(tf.float32, shape=(None,))
        return {'x':x, 'z':tf.norm(x)}


    T = tfModel(scalar_add)
    print T('z', x=2, y=3)
    # KeyError 'q', not in the graph
    # T['q']

    T = tfModel(vector_add)
    print T('z', x=[2,3], y=[4,5])

    T = tfModel(L2norm)
    print T('z', x=[1,2,3])

    # ValueError (wrong shape!)
    # print T('z', x=1)




