from collections import defaultdict
from doy.utils import smooth_ema, smooth_conv
from typing import Optional, Union
import os
import wandb
import doy
import numpy as np


class Logger:
    def __init__(self, use_wandb: bool = True):
        self.data = defaultdict(list)
        self.data_x = defaultdict(list)
        self.use_wandb = use_wandb

    def __call__(self, step: int, **kwargs):
        assert kwargs
        for k, v in list(kwargs.items()):
            if v is None:
                del kwargs[k]
                continue

            try:
                v = v.item()
            except AttributeError:
                pass

            self.data[k].append(v)
            self.data_x[k].append(step)

        if self.use_wandb:
            wandb.log(data=kwargs, step=step)

    def __getitem__(self, key):
        return np.array(self.data[key])

    def get(self, key, smooth_args: Optional[tuple] = ("ema", 0.9)):
        if smooth_args is None:
            return self[key]

        smoothing_method, smoothing_param = smooth_args
        if smoothing_method == "ema":
            return smooth_ema(self[key], smoothing_param)
        elif smoothing_method == "conv":
            return smooth_conv(self[key], smoothing_param)
        else:
            raise ValueError(
                f"Unknown smoothing method: {smoothing_method}, should be 'ema' or 'conv'."
            )

    def save(self, path: Union[str, os.PathLike]):
        doy.dump({"data": self.data, "data_x": self.data_x}, path)
