from enum import Enum


class PressureUnit(str, Enum):
    PASCAL = "Pa"
    KILOPASCAL = "kPa"
    MEGAPASCAL = "mPa"
    BAR = "bar"


class TemperatureUnit(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"


class UnitSystem(str, Enum):
    SI = "SI"
    SI_WITH_CELISUS = "SIC"
    IMPERIAL = "IS"
