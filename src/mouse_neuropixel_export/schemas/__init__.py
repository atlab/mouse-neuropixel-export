import pickle
import numpy as np

from dataclasses import dataclass as _dataclass, fields

def dataclass(cls=None, **dataclass_kwargs):
    def decorate(c):
        c = _dataclass(c, **dataclass_kwargs)

        allowed = {f.name for f in fields(c)}
        orig_init = c.__init__

        def __init__(self, *args, **kwargs):
            if kwargs:
                kwargs = {k: v for k, v in kwargs.items() if k in allowed}
            orig_init(self, *args, **kwargs)

        c.__init__ = __init__
        return c

    return decorate(cls) if cls is not None else decorate


class PickleAdapter:
    def get(self):
        with open(self.get_path('pkl'), 'rb') as f:
            return pickle.load(f)

    def put(self, data):
        with open(self.get_path('pkl'), 'wb') as f:
            pickle.dump(data, f)


class NumpyAdapter:
    def get(self):
        return np.load(self.get_path('npy'))

    def put(self, data):
        np.save(self.get_path('npy'), data)