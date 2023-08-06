import argparse

import pandas as pd

from mixprops.mixture import Mixture
from mixprops.reference_conditions import ReferenceConditions


def run():
    parser = argparse.ArgumentParser(description="Mixture properties calculator.")
    parser.add_argument(
        "-rc",
        "--conditions",
        type=str,
        required=True,
        help="Reference conditions values.",
    )
    parser.add_argument(
        "-u", "--units", type=str, required=True, help="Reference conditions units."
    )
    parser.add_argument("-s", "--species", type=str, required=True, help="Species.")
    parser.add_argument(
        "-sc",
        "--composition",
        type=str,
        required=True,
        help="Molar composition as fractions.",
    )
    args = parser.parse_args()

    conditions = args.conditions.split(",")
    units = args.units.split(",")

    ref_conditions = ReferenceConditions(
        absolute_pressure_unit=units[0],
        temperature_unit=units[1],
        absolute_pressure=float(conditions[0]),
        temperature=float(conditions[1]),
    )

    species = args.species.split(",")
    composition = [float(mf) for mf in args.composition.split(",")]

    if len(species) != len(composition):
        raise ValueError("Species and fractions should be of the same length")

    mixture = Mixture(
        species=list(zip(species, composition)), reference_conditions=ref_conditions
    )

    df = pd.DataFrame.from_dict([mixture.model_dump()])

    print("")
    print(df.T.rename(columns={0: "Value"}))
    print("")
