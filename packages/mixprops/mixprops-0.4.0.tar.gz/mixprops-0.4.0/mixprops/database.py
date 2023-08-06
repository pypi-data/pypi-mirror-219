import os
from typing import List

import pandas as pd

from mixprops.species import Species

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(MODULE_PATH, "data")


class SpeciesNotFoundException(Exception):
    def __init__(self, name: str):
        self.message = f"Species {name} not found"
        super().__init__(self.message)


class Database:
    def __init__(self, species: List[Species]):
        self.species = species

    @classmethod
    def from_file(cls, file: str):
        df = pd.read_csv(DATA_PATH + f"/{file}", index_col=0)
        species_list = df.to_dict(orient="records")
        return cls(species=[Species(**item) for item in species_list])

    def find_species(self, name: str) -> Species:
        species = [
            item for item in self.species if item.species == name or item.name == name
        ]
        if not species:
            raise SpeciesNotFoundException(name=name)
        return species[0]
