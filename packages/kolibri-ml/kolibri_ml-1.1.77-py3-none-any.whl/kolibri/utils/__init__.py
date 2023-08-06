
import json
import logging
import six
from typing import  Optional, Sequence, Union, Collection
import numpy as np

logger = logging.getLogger(__name__)


def overlap(start1, end1, start2, end2):
    return not (end1 <= start2 or start1 >= end2)


def lazyproperty(fn):
    """Allows to avoid recomputing a property over and over.

    The result gets stored in a local var. Computation of the property
    will happen once, on the first call of the property. All
    succeeding calls will use the text stored in the private property."""

    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazyprop


def as_text_type(t):
    if isinstance(t, six.text_type):
        return t
    else:
        return six.text_type(t)



def json_to_string(obj, **kwargs):
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)



def zero_pad_truncate(batch: Sequence[Sequence[Union[int, float, np.integer, np.floating,
                                                     Sequence[Union[int, float, np.integer, np.floating]]]]],
                      max_len: int, pad: str = 'post', trunc: str = 'post',
                      dtype: Optional[Union[type, str]] = None) -> np.ndarray:
    """

    Args:
        batch: assumes a batch of lists of word indexes or their vector representations
        max_len: resulting length of every batch item
        pad: how to pad shorter batch items: can be ``'post'`` or ``'pre'``
        trunc: how to truncate a batch item: can be ``'post'`` or ``'pre'``
        dtype: overrides dtype for the resulting ``ndarray`` if specified,
         otherwise ``np.int32`` is used for 2-d arrays and ``np.float32`` — for 3-d arrays

    Returns:
        a 2-d array of size ``(len(batch), max_len)`` or a 3-d array of size ``(len(batch), max_len, len(batch[0][0]))``
    """
    if isinstance(batch[0][0], Collection):  # ndarray behaves like a Sequence without actually being one
        size = (len(batch), max_len, len(batch[0][0]))
        dtype = dtype or np.float32
    else:
        size = (len(batch), max_len)
        dtype = dtype or np.int32

    padded_batch = np.zeros(size, dtype=dtype)
    for i, batch_item in enumerate(batch):
        if len(batch_item) > max_len:  # trunc
            padded_batch[i] = batch_item[slice(max_len) if trunc == 'post' else slice(-max_len, None)]
        else:  # pad
            padded_batch[i, slice(len(batch_item)) if pad == 'post' else slice(-len(batch_item), None)] = batch_item

    return np.asarray(padded_batch)
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

import re
from typing import List


def enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]