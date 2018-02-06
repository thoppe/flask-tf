import tensorflow as tf
from flask import Flask, request, jsonify

_MODEL = None

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
                x = g.get_tensor_by_name("{}:0".format(k))
                feed_dict[x] = v


            run_vars = []
            for k in out_args:
                x = g.get_tensor_by_name("{}:0".format(k))
                run_vars.append(x)
            
            res = sess.run(run_vars, feed_dict=feed_dict)
            yield res


class tfFlask_caller(object):

    def __init__(self, model_func):
        self.f = tf_coroutine(model_func)
        
    def __call__(self, target, **feed_dict):
        '''
        Calls a single target
        '''
        next(self.f)

        res = self.f.send([feed_dict, [target,]])
                
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

@app.route('/feed', methods=['POST'])
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
