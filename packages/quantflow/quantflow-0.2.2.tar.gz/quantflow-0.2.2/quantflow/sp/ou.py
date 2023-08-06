from __future__ import annotations

from typing import cast

import numpy as np
from pydantic import Field
from scipy.stats import gamma, norm

from ..utils.distributions import Exponential
from ..utils.paths import Paths
from ..utils.types import Vector
from .base import Im, IntensityProcess, StochasticProcess1DMarginal
from .poisson import CompoundPoissonProcess
from .weiner import WeinerProcess


class Vasicek(IntensityProcess):
    bdlp: WeinerProcess = Field(
        default_factory=WeinerProcess,
        description="Background driving Weiner process",
    )
    theta: float = Field(default=1.0, gt=0, description="Mean rate")


class NGOU(IntensityProcess):
    bdlp: CompoundPoissonProcess = Field(
        default_factory=CompoundPoissonProcess,
        description="Background driving Levy process",
    )

    def sample_from_draws(self, draws: Paths, *args: Paths) -> Paths:
        raise NotImplementedError


class GammaOU(NGOU):
    @property
    def intensity(self) -> float:
        return self.bdlp.intensity

    @property
    def beta(self) -> float:
        # TODO: find a better way for this
        return cast(Exponential, self.bdlp.jumps).decay

    @classmethod
    def create(cls, rate: float = 1, decay: float = 1, kappa: float = 1) -> GammaOU:
        return cls(
            rate=rate,
            kappa=kappa,
            bdlp=CompoundPoissonProcess(
                intensity=rate * decay, jumps=Exponential(decay=decay)
            ),
        )

    def marginal(self, t: Vector) -> StochasticProcess1DMarginal:
        return GammaOUMarginal(process=self, t=t)

    def characteristic_exponent(self, t: Vector, u: Vector) -> Vector:
        b = self.beta
        iu = Im * u
        c1 = iu * np.exp(-self.kappa * t)
        c0 = self.intensity * np.log((b - c1) / (b - iu))
        return -c0 - c1 * self.rate

    def cumulative_characteristic(self, t: Vector, u: Vector) -> Vector:
        kappa = self.kappa
        b = self.beta
        iu = Im * u
        iuk = iu / kappa
        ekt = np.exp(-kappa * t)
        c1 = iuk * (1 - ekt)
        c0 = self.intensity * (
            b * np.log(b / (iuk + (b - iuk) / ekt)) / (iuk - b) - kappa * t
        )
        return np.exp(c0 + c1 * self.rate)

    def sample(self, n: int, time_horizon: float = 1, time_steps: int = 100) -> Paths:
        dt = time_horizon / time_steps
        jump_process = self.bdlp
        paths = np.zeros((time_steps + 1, n))
        paths[0, :] = self.rate
        for p in range(n):
            arrivals = jump_process.arrivals(self.kappa * time_horizon)
            jumps = jump_process.sample_jumps(len(arrivals))
            pp = paths[:, p]
            i = 1
            for arrival, jump in zip(arrivals, jumps):
                arrival /= self.kappa
                while i * dt < arrival:
                    i = self._advance(i, pp, dt)
                if i <= time_steps:
                    i = self._advance(i, pp, dt, arrival, jump)
            while i <= time_steps:
                i = self._advance(i, pp, dt)
        return Paths(t=time_horizon, data=paths)

    def _advance(
        self, i: int, pp: np.ndarray, dt: float, arrival: float = 0, jump: float = 0
    ) -> int:
        x = pp[i - 1]
        kappa = self.kappa
        t0 = i * dt
        t1 = t0 + dt
        a = arrival or t1
        pp[i] = x - kappa * x * (a - t0) - kappa * (x + jump) * (t1 - a) + jump
        return i + 1

    def cumulative_characteristic2(self, t: float, u: Vector) -> Vector:
        """Formula from a paper"""
        kappa = self.kappa
        b = self.beta
        iu = Im * u
        iuk = iu / kappa
        ekt = np.exp(-kappa * t)
        c1 = iuk * (1 - ekt)
        c0 = self.intensity * (b * np.log(b / (b - c1)) - iu * t) / (iuk - b)
        return np.exp(c0 + c1 * self.rate)


class GammaOUMarginal(StochasticProcess1DMarginal[GammaOU]):
    def mean(self) -> float:
        return self.process.intensity / self.process.beta

    def variance(self) -> float:
        return self.process.intensity / self.process.beta / self.process.beta

    def pdf(self, x: Vector) -> Vector:
        return gamma.pdf(x, self.process.intensity, scale=1 / self.process.beta)


class VasicekMarginal(StochasticProcess1DMarginal[Vasicek]):
    def mean(self) -> Vector:
        ekt = self.process.ekt(self.t)
        return self.process.rate * ekt + self.process.theta * (1 - ekt)

    def variance(self) -> Vector:
        ekt = self.process.ekt(2 * self.t)
        return 0.5 * self.process.bdlp.sigma2 * (1 - ekt) / self.process.kappa

    def pdf(self, n: Vector) -> Vector:
        return norm.pdf(n, loc=self.mean(), scale=self.std())

    def cdf(self, n: Vector) -> Vector:
        return norm.cdf(n, loc=self.mean(), scale=self.std())
