from typing import Optional

from pydantic import (BaseModel, ConfigDict, Field, FieldValidationInfo,
                      field_validator)

from mixprops.constants import BAR_TO_PA, KELVIN_ADD, KPA_TO_PA, MPA_TO_PA
from mixprops.settings import Settings, get_settings
from mixprops.units import PressureUnit, UnitSystem


class State(BaseModel):
    settings: Optional[Settings] = Field(default_factory=get_settings)
    pressure: float
    temperature: float
    model_config = ConfigDict(use_enum_values=True)

    @field_validator("pressure")
    def validate_pressure(cls, value: float, info: FieldValidationInfo) -> float:
        pressure_unit: PressureUnit = info.data["settings"].pressure_unit
        if pressure_unit == PressureUnit.KILOPASCAL:
            value *= KPA_TO_PA
        elif pressure_unit == PressureUnit.MEGAPASCAL:
            value *= MPA_TO_PA
        elif pressure_unit == PressureUnit.BAR:
            value *= BAR_TO_PA
        return value

    @field_validator("temperature")
    def validate_temperature(cls, value: float, info: FieldValidationInfo) -> float:
        units = info.data["settings"].units
        if units == UnitSystem.SI_WITH_CELISUS:
            value += KELVIN_ADD
        elif units == UnitSystem.IMPERIAL:
            value = (value - 32) * (5 / 9) + KELVIN_ADD
        return value
