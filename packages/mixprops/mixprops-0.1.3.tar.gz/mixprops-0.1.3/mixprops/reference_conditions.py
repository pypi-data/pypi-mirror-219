from enum import Enum

from pydantic import (BaseModel, ConfigDict, FieldValidationInfo,
                      field_validator)

from mixprops.constants import BAR_TO_PA, KELVIN_ADD, KPA_TO_PA, MPA_TO_PA


class AbsolutePressureUnit(str, Enum):
    PASCAL = "Pa"
    KILOPASCAL = "kPa"
    MEGAPASCAL = "mPa"
    BAR = "bar"


class TemperatureUnit(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"


class ReferenceConditions(BaseModel):
    absolute_pressure_unit: AbsolutePressureUnit
    absolute_pressure: float
    temperature_unit: TemperatureUnit
    temperature: float
    model_config = ConfigDict(use_enum_values=True)

    @field_validator("absolute_pressure")
    def validate_absolute_pressure(
        cls, value: float, info: FieldValidationInfo
    ) -> float:
        if info.data["absolute_pressure_unit"] == AbsolutePressureUnit.KILOPASCAL:
            value *= KPA_TO_PA
        elif info.data["absolute_pressure_unit"] == AbsolutePressureUnit.MEGAPASCAL:
            value *= MPA_TO_PA
        elif info.data["absolute_pressure_unit"] == AbsolutePressureUnit.BAR:
            value *= BAR_TO_PA
        return value

    @field_validator("temperature")
    def validate_temperature(cls, value: float, info: FieldValidationInfo) -> float:
        if info.data["temperature_unit"] == TemperatureUnit.CELSIUS:
            value += KELVIN_ADD
        elif info.data["temperature_unit"] == TemperatureUnit.FAHRENHEIT:
            value = (value - 32) * (5 / 9) + KELVIN_ADD
        return value
