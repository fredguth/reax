# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_data.ipynb.

# %% auto 0
__all__ = ['Tensor', 'get_dls', 'collate_dict', 'DataLoaders', 'Batch']

# %% ../nbs/00_data.ipynb 3
from functools import partial
from operator import itemgetter
from typing import NamedTuple, Union

import jax
import jax.numpy as jnp
import lovely_jax as lj
import numpy as np
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, default_collate
import torch

# %% ../nbs/00_data.ipynb 6
def get_dls(train_ds, valid_ds, bs, **kwargs):
    return (DataLoader(train_ds, batch_size=bs, shuffle=True, **kwargs),
            DataLoader(valid_ds, batch_size=bs*2, **kwargs))

def collate_dict(ds):
    get = itemgetter(*ds.features)
    def _f(b): return get(default_collate(b))
    return _f

class DataLoaders:
    def __init__(self, *dls): self.train,self.valid = dls[:2]

    @classmethod
    def from_dd(cls, dd, batch_size, as_tuple=True, **kwargs):
        f = collate_dict(dd['train'])
        return cls(*get_dls(*dd.values(), bs=batch_size, collate_fn=f, **kwargs))

# %% ../nbs/00_data.ipynb 8
Tensor = Union[jax.Array, jnp.ndarray, np.ndarray] # should include torch.Tensor?

class Batch(NamedTuple):
  input: Tensor   # [B, H, W, C]
  target: Tensor  # [B]