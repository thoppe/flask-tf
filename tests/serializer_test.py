from flasktf.serializers import pack, unpack
import numpy as np
from numpy.testing import assert_array_equal


class Serializer_Test:

    @classmethod
    def setup_class(cls):
        pass

    def numpy_array_test(self):
        x = np.random.uniform(size=(50))
        assert_array_equal(x, unpack(pack(x)))

    def numpy_scalar_test(self):
        x = np.random.uniform()
        assert_array_equal(x, unpack(pack(x)))

    def numpy_multiarray_test(self):
        x = np.random.uniform(size=(10, 10, 10))
        assert_array_equal(x, unpack(pack(x)))

    def python_int_test(self):
        x = 3
        assert_array_equal(x, unpack(pack(x)))

    def python_float_test(self):
        x = 3.141
        assert_array_equal(x, unpack(pack(x)))

    def python_array_test(self):
        x = 3.141
        assert_array_equal(x, unpack(pack(x)))
