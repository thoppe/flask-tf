# flask-tf

A simple way to serve your [tensorflow](https://github.com/tensorflow/tensorflow) models with [flask](http://flask.pocoo.org/).

Start a server and run a model:

```python
import tensorflow as tf
from flasktf import serve

def dot_product():
    x = tf.placeholder(tf.float32, shape=(None,),name='x')
    y = tf.placeholder(tf.float32, shape=(None,),name='y')
    return {'x':x, 'y':y, 'z':tf.tensordot(x,y,1)}

serve(dot_product)
```

With the server running,

```python
from flasktf import caller

model = caller()
print model('z', x=[1,2,3], y=[0,1,2])
# Returns {"z": 8.0}
```

if you prefer [Keras](https://keras.io/), simply return the model and the outputs from a call returned in sequential order:

```python
import keras.layers, keras.models
from flasktf import serve

def model(N):
    x = keras.layers.Input(shape=(N,),)
    y = keras.layers.Activation(activation='softmax')(x)
    return keras.models.Model(inputs=x, outputs=y)

serve(dot_product)
```

```python
from flasktf import caller

model = caller()
print model([[1,2,3]])
# Returns {"z": 8.0}
```


### Development notes

If tests fail, try increasing `startup_time` in [tests/caller_test.py](tests/caller_test.py).