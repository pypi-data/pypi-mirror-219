from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from numpy.random import normal
from pydantic import BaseModel, ConfigDict, Field
from scipy.integrate import cumtrapz

from . import plot


class Paths(BaseModel):
    """Paths of a stochastic process"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    t: float = Field(description="time horizon")
    data: np.ndarray = Field(description="paths")

    @property
    def dt(self) -> float:
        return self.t / self.time_steps

    @property
    def samples(self) -> int:
        return self.data.shape[1]

    @property
    def time_steps(self) -> int:
        return self.data.shape[0] - 1

    @property
    def time(self) -> np.ndarray:
        return np.linspace(0.0, self.t, num=self.time_steps + 1)

    @property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame(self.data, index=self.time)

    @property
    def xs(self) -> list[np.ndarray]:
        """Time as list of list (for visualization tools)"""
        return self.samples * [self.time]

    @property
    def ys(self) -> list[list[float]]:
        """Paths as list of list (for visualization tools)"""
        return self.data.transpose().tolist()

    def mean(self) -> np.ndarray:
        """Mean of paths"""
        return np.mean(self.data, axis=1)

    def std(self) -> np.ndarray:
        """Standard deviation of paths"""
        return np.std(self.data, axis=1)

    def var(self) -> np.ndarray:
        """Variance of paths"""
        return np.var(self.data, axis=1)

    def integrate(self) -> Paths:
        """Integrate paths"""
        return self.__class__(
            t=self.t, data=cumtrapz(self.data, dx=self.dt, axis=0, initial=0)
        )

    def plot(self, **kwargs: Any) -> Any:
        return plot.plot_lines(self.df, **kwargs)

    @classmethod
    def normal_draws(
        cls,
        paths: int,
        time_horizon: float,
        time_steps: int = 1000,
        antithetic_variates: bool = True,
    ) -> Paths:
        """Generate normal draws

        paths: number of paths
        time_horizon: time horizon
        time_steps: number of time steps to arrive at horizon
        """
        time_horizon / time_steps
        odd = 0
        if antithetic_variates:
            odd = paths % 2
            paths = paths // 2
        data = normal(size=(time_steps + 1, paths))
        if antithetic_variates:
            data = np.concatenate((data, -data), axis=1)
            if odd:
                extra_data = normal(size=(time_steps + 1, odd))
                data = np.concatenate((data, extra_data), axis=1)
        return cls(t=time_horizon, data=data)
