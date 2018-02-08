import pylru
import tensorflow as tf

'''
def L2norm():
    x = tf.placeholder(tf.float32, shape=(None,), name='x')
    z = tf.add(x,x,name='z')
    #tf.norm(x, name='z')
'''

def scalar_add():
    x = tf.placeholder(tf.float32, name='x')
    y = tf.placeholder(tf.float32, name='y')
    z = tf.add(x,y,name='z')

class tfModel(object):

    def __init__(self, model_func):
         config = tf.ConfigProto()
         config.gpu_options.allow_growth = True
         with tf.Graph().as_default() as self.g:
             self.sess = tf.Session(config=config)
             model_func()
             #print self.g.get_operation_by_name('z')
             #print [x.name for x in self.sess.graph.get_operations()]
             #print [n.name for n in tf.get_default_graph().as_graph_def().node]
             #exit()

    def __getitem__(self, key, loc=0):

        try:
            val = self.g.get_tensor_by_name("{}:{}".format(key, loc))
        except KeyError:
            msg = "{}:{} is not defined in the model"
            raise KeyError(msg.format(key,loc))
        return val

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
        
from tqdm import tqdm
    
T = tfModel(scalar_add)
print T.get_info('x')
print T.get_info('z')

print T('z', x=2, y=3)
exit()

