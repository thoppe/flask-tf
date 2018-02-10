import numpy as np
import StringIO


def unpack(serialized):
    memfile = StringIO.StringIO()
    memfile.write(serialized)
    memfile.seek(0)
    return np.load(memfile)


def pack(x):
    memfile = StringIO.StringIO()
    np.save(memfile, x)
    memfile.seek(0)
    return memfile.read()
