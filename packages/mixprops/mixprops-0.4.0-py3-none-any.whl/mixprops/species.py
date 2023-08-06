import math
from typing import Optional

from pydantic import BaseModel, computed_field

from mixprops.constants import MU_CONSTANT, R_U, A, B, C, D, E, F
from mixprops.state import State


class Species(BaseModel):
    name: str
    species: str
    sigma: float
    eta: float
    molecular_weight: float
    a1: float
    a2: float
    a3: float
    a4: float
    a5: float
    a6: float
    a7: float
    a8: Optional[float]
    a9: Optional[float]


class MixtureSpecies(BaseModel):
    state: State
    species: Species
    mole_fraction: float

    @computed_field
    @property
    def mass(self) -> float:
        return self.mole_fraction * self.species.molecular_weight

    @computed_field
    @property
    def R(self) -> float:
        return R_U / self.species.molecular_weight

    @computed_field
    @property
    def heat_capacity(self) -> float:
        return self.R * (
            (self.species.a1 * self.state.temperature**-2)
            + (self.species.a2 * self.state.temperature**-1)
            + (self.species.a3)
            + (self.species.a4 * self.state.temperature)
            + (self.species.a5 * self.state.temperature**2)
            + (self.species.a6 * self.state.temperature**3)
            + (self.species.a7 * self.state.temperature**4)
        )

    @computed_field
    @property
    def t_star(self) -> float:
        return self.state.temperature / self.species.eta

    @computed_field
    @property
    def omega(self) -> float:
        return (
            A * (self.t_star**-B)
            + C * (math.exp(-D * self.t_star))
            + E * (math.exp(-F * self.t_star))
        )

    @computed_field
    @property
    def mu(self) -> float:
        return (
            MU_CONSTANT
            * math.sqrt(self.species.molecular_weight * self.state.temperature)
        ) / (self.species.sigma**2 * self.omega)

    @computed_field
    @property
    def k(self) -> float:
        return (
            (15 / 4)
            * (R_U / self.species.molecular_weight)
            * self.mu
            * (
                (4 / 15) * ((self.heat_capacity * self.species.molecular_weight) / R_U)
                + 1 / 3
            )
        )
