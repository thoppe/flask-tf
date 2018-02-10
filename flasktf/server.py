from flask import Flask, request, jsonify, abort
from default_caller import MODEL
from serializers import pack, unpack

app = Flask(__name__)

@app.route('/')
def index():
    msg = '''Endpoints:\n/check\nserve'''
    return msg.strip()

@app.route('/info', methods=['POST'])
def info():    
    js = request.json
    if not js:
        return jsonify(MODEL.var.keys()), 200

    data = {}
    for name in js:
        data[name] = MODEL.get_info(name)
        
    return jsonify(data), 200

@app.route('/serve', methods=['POST'])
def process():
    assert(MODEL is not None)

    print vars(request)

    feed_args = {}
    targets = None
    
    for k,v in request.files.items():
        if k != "_targets":
            feed_args[k] = unpack(v.read())
        else:
            targets = unpack(v.read())

    assert(targets is not None)

    result = MODEL(*targets, **feed_args)
    serialized = pack(result)

    return serialized, 200
    
def run():
    app.run(debug=True)
