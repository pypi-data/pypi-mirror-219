import itertools
import numpy as np
import matplotlib.pyplot as plt
from typing import Any, List, Union, Tuple, Dict


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def mappend(lists, values):
    for l, v in zip(lists, values):
        l.append(v)


def lerp(a, b, alpha=0.9):
    return alpha * a + (1 - alpha) * b


def smooth_ema(X, alpha=0.9):
    assert 0 <= alpha < 1
    if len(X) == 0:
        return X
    res = []
    z = X[0]
    for x in X:
        z = lerp(z, x, alpha)
        res.append(z)
    return np.array(res)


def smooth_conv(X, box_pts, mode="valid"):
    assert isinstance(box_pts, int)
    if len(X) == 0:
        return X
    box = np.ones(box_pts) / box_pts
    X_smooth = np.convolve(X, box, mode=mode)
    return X_smooth


def bchw_to_bhwc(x):
    assert len(x.shape) == 4
    if isinstance(x, np.ndarray):
        return x.transpose(0, 2, 3, 1)
    else:
        return x.permute(0, 2, 3, 1)


def bhwc_to_bchw(x):
    assert len(x.shape) == 4
    if isinstance(x, np.ndarray):
        return x.transpose(0, 3, 1, 2)
    else:
        return x.permute(0, 3, 1, 2)


def count_parameters(model, requires_grad_only=True):
    return sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad or not requires_grad_only
    )


def state_dict_orig(m):
    return m._orig_mod.state_dict() if hasattr(m, "_orig_mod") else m.state_dict()  # type: ignore


def get_params_from_modules(*modules):
    yield from itertools.chain(*[m.parameters() for m in modules])


class Schedule:
    def __call__(self, step: Union[int, np.ndarray, list]):
        """Returns the value of the schedule at the given step(s)"""
        raise NotImplementedError()

    @property
    def range(self) -> Any:
        """
        Returns the range of the schedule.
        This range is what .plot() plots, __call__ may accept values outside this range.
        """
        raise NotImplementedError()

    def plot(self):
        xs = np.arange(*self.range)
        plt.plot(xs, self(xs))
        plt.show()


class PiecewiseLinearSchedule(Schedule):
    def __init__(self, points, values):
        self.points = np.array(points)
        self.values = np.array(values)
        if not np.all(np.diff(points) > 0):
            raise ValueError("points must be monotonically increasing")
        if len(self.points) != len(self.values):
            raise ValueError("points and values need to be of the same length")

    @property
    def range(self):
        return self.points[0], self.points[-1]

    def __call__(self, step: Union[int, np.ndarray, list]):
        is_scalar = False
        if isinstance(step, int):
            step = np.array([step])
            is_scalar = True
        elif isinstance(step, list):
            step = np.array(step)

        if np.any(step < self.points[0]) or np.any(self.points[-1] < step):
            raise ValueError("t must be in the interval [points[0], points[-1]]")

        inds = np.searchsorted(self.points, step) - 1
        inds = np.clip(inds, 0, len(self.points) - 2)

        interp = (step - self.points[inds]) / (
            self.points[inds + 1] - self.points[inds]
        )
        result = self.values[inds] * (1 - interp) + self.values[inds + 1] * interp

        return result[0] if is_scalar else result


# get_params


class LRScheduler:
    def __init__(
        self,
        opt_cls,
        param_groups: Dict[str, Tuple[Schedule, List["torch.nn.Module"]]],
        **kwargs,
    ):
        opt_param_groups = []
        self.schedules = []

        for name, (schedule, modules) in param_groups.items():
            opt_param_groups.append(
                {"params": get_params_from_modules(*modules), "lr": schedule(0)}
            )
            self.schedules.append((name, schedule))

        self.opt = opt_cls(params=opt_param_groups, **kwargs)

    @classmethod
    def make(
        cls,
        opt_cls,
        param_groups: Dict[str, Tuple[Schedule, List["torch.nn.Module"]]],
        **kwargs,
    ):
        scheduler = cls(opt_cls, param_groups, **kwargs)
        return scheduler.opt, scheduler

    def step(self, step):
        for pg, (_, schedule) in zip(self.opt.param_groups, self.schedules):
            pg["lr"] = schedule(step)

    def get_state(self):
        return {
            "lr_" + name: pg["lr"]
            for pg, (name, _) in zip(self.opt.param_groups, self.schedules)
        }


def normalize_into_range(lower, upper, v, ensure_in_range=False):
    assert lower <= upper
    if ensure_in_range and (v < lower or v > upper):
        raise ValueError(f"Value {v} is not in range [{lower}, {upper}]")

    return (v - lower) / (upper - lower)
