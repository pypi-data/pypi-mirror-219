# mixprops

[![CI](https://github.com/oaarnikoivu/mixprops/workflows/CI/badge.svg)](https://github.com/oaarnikoivu/mixprops/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![pypi](https://img.shields.io/pypi/v/mixprops)](https://pypi.org/project/mixprops/)
[![versions](https://img.shields.io/pypi/pyversions/mixprops.svg)](https://github.com/oaarnikoivu/mixprops)
[![license](https://img.shields.io/github/license/oaarnikoivu/mixprops.svg)](https://github.com/oaarnikoivu/mixprops/blob/main/LICENSE)

Mixture properties calculator.

## Installation

### Python

```bash
pip install mixprops
```

### CLI

Follow instructions from [pipx](https://github.com/pypa/pipx) to install `pipx`.

```bash
pipx install git+https://github.com/oaarnikoivu/mixprops.git
```

## Usage

### Python

```python
from mixprops.mixture import Mixture
from mixprops.reference_conditions import ReferenceConditions

mixture = Mixture(
    species=[("O2", 0.21), ("N2", 0.79)],
    reference_conditions=ReferenceConditions(
        absolute_pressure_unit="Pa",
        absolute_pressure=101325,
        temperature_unit="C",
        temperature=25
    ))

print(mixture.specific_heat_capacity)
# 1011.338752
```

### CLI

```bash
mixprops \
    -rc 101325,25 \
    -u Pa,C \
    -s O2,N2 \
    -sc 0.21,0.79
```

- rc = Reference conditions -> Absolute pressure,temperature
- u = Reference condition units -> Pressure unit,temperature unit
- s = Comma separated list of species by name or species -> O2,N2 or Oxygen,Nitrogen
- sc = Species molar composition as comma separated mole fractions -> 0.21,0.79

### Properties

- `molecular_weight` - Molecular weight (g/mol)
- `density` - Density (kg/m3)
- `specific_heat_capacity` - Specific heat capacity (J/kg-K)
- `viscosity` - Viscosity (kg/m-s)
- `conductivity` - Thermal conductivity (W/m-K)
- `speed_of_sound` - Speed of sound (m/s)
- `adiabatic_index` - Adiabatic index

### Supported species

For the supported species, see the `.csv` files in the `mixprops/data` directory.
