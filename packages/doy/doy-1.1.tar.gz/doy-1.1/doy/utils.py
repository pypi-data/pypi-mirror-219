import numpy as np
import matplotlib.pyplot as plt
from typing import Union


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


class PiecewiseLinearSchedule:
    def __init__(self, points, values):
        self.points = np.array(points)
        self.values = np.array(values)
        if not np.all(np.diff(points) > 0):
            raise ValueError("points must be monotonically increasing")
        if len(self.points) != len(self.values):
            raise ValueError("points and values need to be of the same length")

    def __call__(self, t: Union[int, np.ndarray, list]):
        is_scalar = False
        if isinstance(t, int):
            t = np.array([t])
            is_scalar = True
        elif isinstance(t, list):
            t = np.array(t)

        if np.any(t < self.points[0]) or np.any(self.points[-1] < t):
            raise ValueError("t must be in the interval [points[0], points[-1]]")

        inds = np.searchsorted(self.points, t) - 1
        inds = np.clip(inds, 0, len(self.points) - 2)

        interp = (t - self.points[inds]) / (self.points[inds + 1] - self.points[inds])
        result = self.values[inds] * (1 - interp) + self.values[inds + 1] * interp

        return result[0] if is_scalar else result

    def plot(self):
        xs = np.arange(0, self.points[-1])
        plt.plot(xs, self(xs))
        plt.show()
