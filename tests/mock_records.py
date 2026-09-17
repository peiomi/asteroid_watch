from src.etl.models import AsteroidRecord

MOCK_RECORDS = [
    # low risk
    AsteroidRecord(
        id="1",
        name="Tiny Tim",
        diameter_min=0.05,
        diameter_max=0.10,
        miss_distance_km=50_000_000.0,
        relative_velocity_km_s=5.0,
        is_hazardous=False,
        close_approach_date="2026-01-01",
    ),
    # medium risk
    AsteroidRecord(
        id="2",
        name="Medium Mike",
        diameter_min=0.25,
        diameter_max=0.50,
        miss_distance_km=10_000_000.0,
        relative_velocity_km_s=15.0,
        is_hazardous=True,
        close_approach_date="2026-01-02",
    ),
    # high risk
    AsteroidRecord(
        id="3",
        name="Danger Dave",
        diameter_min=0.75,
        diameter_max=1.00,
        miss_distance_km=2_000_000.0,
        relative_velocity_km_s=25.0,
        is_hazardous=True,
        close_approach_date="2026-01-03",
    ),
    # extremely high risk
    AsteroidRecord(
        id="4",
        name="Apocalypse Andy",
        diameter_min=1.50,
        diameter_max=2.00,
        miss_distance_km=500_000.0,
        relative_velocity_km_s=35.0,
        is_hazardous=True,
        close_approach_date="2026-01-04",
    ),
]
