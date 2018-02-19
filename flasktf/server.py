from flask import Flask, request, jsonify
from serializers import pack, unpack
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
MODEL = None

@app.route('/', methods=['GET'])
def index():
    endpoints = ['info', 'serve']
    return jsonify(endpoints), 200


@app.route('/info', methods=['POST'])
def info():
    js = request.json
    if not js:
        return jsonify(MODEL.get_variables().keys()), 200

    data = {}
    for name in js:
        data[name] = MODEL.get_info(name)

    return jsonify(data), 200


@app.route('/tfcall', methods=['POST'])
def tfcall():  # pragma: no cover
    assert(MODEL is not None)

    if(MODEL.name != "tfModel"):
        msg = "server/caller model mismatch, {}/{}"
        raise BadRequest(msg.format(MODEL.name, "tfModel"))
    
    feed_args = {}
    targets = None

    for k, v in request.files.items():
        if k != "_targets":
            feed_args[k] = unpack(v.read())
        else:
            targets = unpack(v.read())

    assert(targets is not None)

    result = MODEL(*targets, **feed_args)
    serialized = pack(result)

    return serialized, 200

@app.route('/kerascall', methods=['POST'])
def kerascall():  # pragma: no cover
    assert(MODEL is not None)

    if(MODEL.name != "kerasModel"):
        msg = "server/caller model mismatch, {}/{}"
        raise BadRequest(msg.format(MODEL.name, "kerasModel"))
    
    print request.files.items()
    print "DIE HERE SERVER"
    exit()
    feed_args = []
    for v in request.files.items():
        if k != "_targets":
            feed_args[k] = unpack(v.read())
        else:
            targets = unpack(v.read())


    print "HERE!!!!!!!!!!!!!!!!!!!!!!!!!"
    exit()
