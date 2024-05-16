from typing import Annotated

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class ValidatedSettings(BaseSettings):
    class Config:
        env_prefix: str = ""

    @field_validator("*")
    @classmethod
    def present(cls, value: str, info: ValidationInfo) -> str:
        if value == "" or value is None:
            variable = f"{cls.Config.env_prefix}{info.field_name}".upper()
            raise ValueError(f"Missing: {variable}")

        return value


ValidatedString = Annotated[str, Field(validate_default=True)]
