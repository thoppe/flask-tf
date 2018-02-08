import tensorflow as tf
from flask import Flask, request, jsonify, abort

_MODEL = None

def _get_tensor(name):
    g = tf.get_default_graph()
    return g.get_tensor_by_name("{}:0".format(name))

def tf_coroutine(model_func):

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    with tf.Graph().as_default() as g:
        sess = tf.Session(config=config)
        model_func()

        while True:
            in_args, out_args = yield

            feed_dict = {}
            for k,v in in_args.items():
                x = _get_tensor(k)
                print x, x.dtype
                print k,v
                exit()
                feed_dict[x] = v


            run_vars = []
            for k in out_args:
                x = _get_tensor(k)
                run_vars.append(x)
            
            res = sess.run(run_vars, feed_dict=feed_dict)
            yield res


class tfFlask_caller(object):

    def __init__(self, model_func):
        self.f = tf_coroutine(model_func)
        next(self.f)
        
    def __call__(self, target, **feed_dict):
        '''
        Calls a single target
        '''
        res = self.f.send([feed_dict, [target,]])
        next(self.f)
                
        # Convert to native python types before returning
        return [x.item() for x in res][0]

def register(model_func):
    global _MODEL
    _MODEL = tfFlask_caller(model_func)

#################################################################

app = Flask(__name__)

@app.route('/')
def index():
    msg = '''Endpoints:\n/feed'''
    return msg.strip()

@app.route('/check', methods=['POST'])
def check():
    js = request.json
    if not js: abort(400)
    for name in js:
        print _get_tensor(name)
        
    return jsonify(js), 200

@app.route('/predict', methods=['POST'])
def process():
    global _MODEL
    assert(_MODEL is not None)
    js = request.json
    if not js or not 'target' in js:
        abort(400)

    target = js.pop('target')
    result = _MODEL(target, **js)

    return jsonify({target:result}), 200

def run():
    app.run(debug=True)
