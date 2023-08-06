import argparse

import pandas as pd

from mixprops.mixture import Mixture
from mixprops.settings import get_settings
from mixprops.state import State

settings = get_settings()


def cli():
    parser = argparse.ArgumentParser(description="Mixture properties calculator.")
    parser.add_argument("--units", type=str, required=False, help="System units")
    parser.add_argument(
        "--pressure-unit", type=str, required=False, help="Pressure unit"
    )
    parser.add_argument(
        "--state",
        type=str,
        required=True,
        help="Mixture state",
    )
    parser.add_argument("--species", type=str, required=True, help="Species")
    parser.add_argument(
        "--composition",
        type=str,
        required=True,
        help="Molar composition as fractions.",
    )
    args = parser.parse_args()

    if args.units:
        settings.units = args.units
    if args.pressure_unit:
        settings.pressure_unit = args.pressure_unit

    state = args.state.split(",")

    state = State(
        settings=settings,
        pressure=float(state[0]),
        temperature=float(state[1]),
    )

    species = args.species.split(",")
    composition = [float(mf) for mf in args.composition.split(",")]

    if len(species) != len(composition):
        raise ValueError("Species and fractions should be of the same length")

    mixture = Mixture(species=list(zip(species, composition)), state=state)

    df = pd.DataFrame.from_dict([mixture.model_dump()])

    print("")
    print(df.T.rename(columns={0: "Value"}))
    print("")
