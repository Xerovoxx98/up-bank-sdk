"""Base model classes for the Up Bank SDK."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UpModel(BaseModel):
    """Base model with common configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
        from_attributes=True,
    )


class MoneyObject(UpModel):
    """Money representation as returned by the API."""

    currency_code: str = Field(alias="currencyCode")
    value: str
    value_in_base_units: int = Field(alias="valueInBaseUnits")
