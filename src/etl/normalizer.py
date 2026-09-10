class Normalizer:
    def normalize(self, data):
        records = {}
        NEO = data["near_earth_objects"]

        for date in NEO:
            for asteroid in NEO[date]:
                record = {
                    "id": asteroid["id"],
                    "name": asteroid["name"],
                    "diameter_min": asteroid[
                        "estimated_diameter.kilometers.estimated_diameter_min"
                    ],
                    "diameter_max": asteroid[
                        "estimated_diameter.kilometers.estimated_diameter_max"
                    ],
                    "miss_distance_km": asteroid[
                        "close_approach_data[0].miss_distance.kilometers"
                    ],
                    "relative_velocity_km_s": asteroid[
                        "close_approach_data[0].relative_velocity.kilometers_per_second"
                    ],
                    "is_hazardous": asteroid["is_potentially_hazardous_asteroid"],
                    "close_approach_date": asteroid[
                        "close_approach_data[0].close_approach_date"
                    ],
                }
                records[record.id] = record

        return records
