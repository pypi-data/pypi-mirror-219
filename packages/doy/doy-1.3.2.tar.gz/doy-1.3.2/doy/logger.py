from collections import defaultdict
from typing import Optional

import numpy as np

from doy.utils import smooth_conv, smooth_ema


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
            import wandb

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

    @property
    def keys(self):
        return list(self.data.keys())

    # def asdict(self):
    #    return {"data": self.data, "data_x": self.data_x}
