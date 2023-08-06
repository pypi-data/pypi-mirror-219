import dataclasses
import logging
from pathlib import Path
import json
import numpy as np


__ALL__ = [
    "NumpyEncoder",
    # "IOEncoder",
    "JsonEncoder",
]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, range):
            value = list(obj)
            return [value[0], value[-1] + 1]
        return super().default(obj)


# class IOEncoder(NumpyEncoder):
#     def default(self, obj):
#         if isinstance(obj, BaseIO):
#             return obj.to_dict()
#         return super().default(obj)


class JsonEncoder(NumpyEncoder):
    """General purpose encode"""

    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if isinstance(obj, Path):
            return obj.absolute()
        if hasattr(obj, "to_dict"):
            return getattr(obj, "to_dict")()
        return super().default(obj)


log = logging.getLogger(__name__)
