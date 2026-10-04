from src.etl.models import AsteroidRecord
import logging

logger = logging.getLogger(__name__)


class Normalizer:
    def normalize(self, data):
        records = []
        neo = data.get("near_earth_objects", {})

        required_fields = [
            "id",
            "name",
            "estimated_diameter",
            "close_approach_data",
            "is_potentially_hazardous_asteroid",
        ]
        for date in neo:
            for asteroid in neo[date]:
                if not all(field in asteroid for field in required_fields):
                    logger.warning(
                        "Skipping asteroid %s due to missing required fields",
                        asteroid.get("id", "unknown"),
                    )
                    continue
                try:
                    record = AsteroidRecord(
                        id=asteroid["id"],
                        name=asteroid["name"],
                        diameter_min=asteroid["estimated_diameter"]["kilometers"][
                            "estimated_diameter_min"
                        ],
                        diameter_max=asteroid["estimated_diameter"]["kilometers"][
                            "estimated_diameter_max"
                        ],
                        miss_distance_km=float(
                            asteroid["close_approach_data"][0]["miss_distance"][
                                "kilometers"
                            ]
                        ),
                        relative_velocity_km_s=float(
                            asteroid["close_approach_data"][0]["relative_velocity"][
                                "kilometers_per_second"
                            ]
                        ),
                        is_hazardous=asteroid["is_potentially_hazardous_asteroid"],
                        close_approach_date=asteroid["close_approach_data"][0][
                            "close_approach_date"
                        ],
                    )
                    records.append(record)
                except (KeyError, IndexError, ValueError, TypeError) as error:
                    logger.warning(
                        "Skipping asteroid %s: %s", asteroid.get("id"), error
                    )
                    continue
        logger.info("Normalized %s asteroid records", len(records))
        return records
