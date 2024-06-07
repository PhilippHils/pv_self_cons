from pydantic import BaseModel, Field


class _Shading(BaseModel):
    average: float = Field(description="Average shading factor in %")


class PvSystem(BaseModel):
    capacity: float = Field(description="Installed capacity in kW")
    tilt: float = Field(description="Tilt angle in degrees")
    azimuth: float = Field(description="Azimuth angle in degrees")
    shading: _Shading = Field(description="Shading factor specification")
    latitude: float = Field(description="Latitude in degrees")
    longitude: float = Field(description="Longitude in degrees")


class Consumer(BaseModel):
    profile: str = Field(description="Consumer profile")
    annual_consumption: float = Field(description="Annual consumption in kWh")


class RunRequestBody(BaseModel):
    pvsystems: list[PvSystem]
    consumers: list[Consumer]
