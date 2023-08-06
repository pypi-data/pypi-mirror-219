from typing import List, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, computed_field

from mixprops.constants import R_U
from mixprops.database import Database
from mixprops.species import MixtureSpecies
from mixprops.state import State


def is_valid_composition(number: float, total: float) -> bool:
    return 0 <= number <= total


class Mixture(BaseModel):
    species: List[Tuple[str, float]] = Field(repr=False, exclude=True)
    state: State = Field(repr=False, exclude=True)
    df: pd.DataFrame = Field(repr=False, exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(
        self,
        species: List[Tuple[str, float]],
        state: State,
    ):
        total = 1.0
        composition = [spec[1] for spec in species]

        if not all(is_valid_composition(value, total) for value in composition):
            raise ValueError("Invalid species composition, expecting fraction format")

        if abs(sum(composition) - total) > 1e-6:
            raise ValueError(f"Invalid species composition, they should sum to {total}")

        db: Database = Database.from_file(
            file="species_T_200_1000.csv"
            if state.temperature <= 1000
            else "species_T_1000_6000.csv"
        )
        relevant_species: List[MixtureSpecies] = []

        for spec in species:
            relevant_spec = db.find_species(name=spec[0])
            relevant_species.append(
                MixtureSpecies(
                    species=relevant_spec,
                    mole_fraction=spec[1],
                    state=state,
                )
            )

        temp_df = pd.DataFrame.from_records(
            data=[spec.model_dump() for spec in relevant_species]
        )
        species_df = pd.json_normalize(temp_df.species)
        temp_df.drop(columns=["species", "state"], inplace=True)
        df = pd.concat([temp_df, species_df], axis=1)
        df["mass_fraction"] = df.mass / df.mass.sum()
        df["mass_ovr_mole_weight"] = df.mass_fraction / df.molecular_weight
        super().__init__(species=species, state=state, df=df)

    @computed_field
    @property
    def molecular_weight(self) -> np.float64:
        return self.df.mole_fraction @ self.df.molecular_weight

    @computed_field
    @property
    def density(self) -> np.float64:
        return (self.state.pressure) / (
            R_U * (self.state.temperature) * self.df.mass_ovr_mole_weight.sum()
        )

    @computed_field
    @property
    def specific_heat_capacity(self) -> np.float64:
        return self.df.mass_fraction @ self.df.heat_capacity

    @computed_field
    @property
    def viscosity(self) -> np.float64:
        viscosity = 0
        for i in range(len(self.df)):
            series_i = self.df.iloc[i]
            num = series_i.mole_fraction * series_i.mu
            theta_num = (
                1
                + np.sqrt(series_i.mu / self.df.mu)
                * (self.df.molecular_weight / series_i.molecular_weight) ** 0.25
            ) ** 2
            theta_den = np.sqrt(
                (8 * (1 + (series_i.molecular_weight / self.df.molecular_weight)))
            )
            theta = theta_num / theta_den
            den = self.df.mole_fraction @ theta
            viscosity += num / den
        return viscosity

    @computed_field
    @property
    def conductivity(self) -> np.float64:
        conductivity = 0
        for i in range(len(self.df)):
            series_i = self.df.iloc[i]
            num = series_i.mole_fraction * series_i.k
            theta_num = (
                1
                + np.sqrt(series_i.mu / self.df.mu)
                * (self.df.molecular_weight / series_i.molecular_weight) ** 0.25
            ) ** 2
            theta_den = np.sqrt(
                (8 * (1 + (series_i.molecular_weight / self.df.molecular_weight)))
            )
            theta = theta_num / theta_den
            den = self.df.mole_fraction @ theta
            conductivity += num / den
        return conductivity

    @computed_field
    @property
    def adiabatic_index(self) -> np.float64:
        return self.specific_heat_capacity / (
            self.specific_heat_capacity - (R_U / self.molecular_weight)
        )

    @computed_field
    @property
    def speed_of_sound(self) -> np.float64:
        return np.sqrt(
            (
                self.adiabatic_index
                * (R_U / self.molecular_weight)
                * (self.state.temperature)
            )
        )
