from dataclasses import dataclass, field
from datetime import datetime, UTC


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
    processed_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class RiskScore:
    id: str
    name: str
    size: str
    speed: str
    distance: str
    risk_score: int
    risk_level: str
    processed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
