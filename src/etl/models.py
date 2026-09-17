from dataclasses import dataclass


@dataclass
class AsteroidRecord:
    id: str
    name: str
    diameter_min: float
    diameter_max: float
    miss_distance_km: float
    relative_velocity_km_s: float
    is_hazardous: bool
    close_approach_date: str


@dataclass
class RiskScore:
    id: str
    name: str
    size: str
    speed: str
    distance: str
    risk_score: int
    risk_level: str
