import numpy as np

from keras.models import Model, Sequential
from keras.layers import Input, Dense, Activation
from flasktf.model_session import baseModelSession

class kerasModelSession(baseModelSession):

    def set_model(self, model_func, *args, **kwargs):
        self.configTF()

        self.model = model_func(*args, **kwargs)
        
        # Define the inputs and outputs with generic names
        self.var = {}

        for n,p in enumerate(self.model.inputs):
            self.var["input{}".format(n)] = p

        for n,p in enumerate(self.model.outputs):
            self.var["output{}".format(n)] = p
    
    def __call__(self, *targets):
        if self.sess is None:
            raise ValueError("set_model has not been run")

        return self.model.predict(*targets)


def sample_model_api(N):
    a = Input(shape=(N,), name='a')
    b = Dense(N)(a)
    c = Activation(activation='softmax')(b)
    model = Model(inputs=a, outputs=c)
    return model

def sample_seq_api(N):
    model = Sequential()
    model.add( Dense(N, input_shape = (N,)) )
    model.add( Activation(activation='softmax') )
    return model

#print sample_seq_api(3)
#exit()

func = sample_model_api
func = sample_seq_api

N = 4
K = kerasModelSession(func, N=N)
x = np.random.uniform(size=(10,N))
print K(x)
print K.get_variables()
print K['input0']
print K.get_info('input0')


#print model
#print model.inputs
#print model.outputs
#print model.layers
#exit()
#x = np.random.uniform(size=(10,N))
#print x
#print model.predict(x)


