from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings

from mixprops.units import PressureUnit, UnitSystem


class Settings(BaseSettings):
    units: UnitSystem = Field(default=UnitSystem.SI_WITH_CELISUS)
    pressure_unit: Optional[PressureUnit] = Field(default=PressureUnit.PASCAL)


def get_settings() -> Settings:
    try:
        with open("settings.yaml") as file:
            settings_yaml = yaml.safe_load(file)
            settings = Settings.model_validate(settings_yaml)
    except IOError:
        settings = Settings()
    return settings
