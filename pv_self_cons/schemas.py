from pydantic import BaseModel, Field


class Shading(BaseModel):
    average: float = Field(default=0.1, description="Average shading factor in %")


class PvSystem(BaseModel):
    capacity: float = Field(default=5.0, description="Installed capacity in kW")
    tilt: float = Field(default=15.0, description="Tilt angle in degrees")
    azimuth: float = Field(default=180.0, description="Azimuth angle in degrees; 180 = south")
    shading: Shading = Field(description="Shading factor specification")
    latitude: float = Field(default=49.0, description="Latitude in degrees")
    longitude: float = Field(default=12.0, description="Longitude in degrees")


class Consumer(BaseModel):
    profile: str = Field(default="H0", description="Consumer profile")
    annual_consumption: float = Field(default=3000.0, description="Annual consumption in kWh")


class RunRequestBody(BaseModel):
    pvsystems: list[PvSystem]
    consumers: list[Consumer]
