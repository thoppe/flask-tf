# flask-tf

A simple way to serve your [tensorflow](https://github.com/tensorflow/tensorflow) models with [flask](http://flask.pocoo.org/).

Start a server and run a model:

```python

def dot_product():
    x = tf.placeholder(tf.float32, shape=(None,),name='x')
    y = tf.placeholder(tf.float32, shape=(None,),name='y')
    return {'x':x, 'y':y, 'z':tf.tensordot(x,y,1)}

serve(dot_product)
```

With the server running,

```python
import requests
url = "http://127.0.0.1:5000/feed"
args = {"x":3, "y":4, "target":"z"}
print requests.post(url, json=args).content

# Returns {"z": 7.0}
```