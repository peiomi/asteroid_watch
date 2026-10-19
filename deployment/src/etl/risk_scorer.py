from deployment.src.etl.models import RiskScore


class RiskScorer:
    LUNAR_DISTANCE_KM = 384_000.0  # 1 lunar distance
    NASA_PHA_KM = 7_480_000.0  # nasa pha distance limit

    def score_risk(self, records):
        risk_scores = []

        for record in records:
            total = 0

            # is hazardous flag
            hazardous_score = self._calc_hazard(record)
            total += hazardous_score

            # size of that thang
            size_score = self._calc_size(record)
            total += size_score[0]

            # how fast that mf is
            velocity_score = self._calc_velocity(record)
            total += velocity_score[0]

            # how close
            distance_score = self._calc_distance(record)
            total += distance_score[0]

            rounded_total = round(total)

            score = RiskScore(
                id=record.id,
                name=record.name,
                size=size_score[1],
                speed=velocity_score[1],
                distance=distance_score[1],
                risk_score=rounded_total,
                risk_level=self._calc_risk_level(rounded_total),
            )
            risk_scores.append(score)

        return risk_scores

    def _calc_hazard(self, record):
        if record.is_hazardous:
            return 40
        return 0

    def _calc_size(self, record):
        diameter = (record.diameter_min + record.diameter_max) / 2

        if diameter <= 0.14:
            score = self._interpolate(diameter, 0.0, 0.14, 0.0, 5.0)
            size = "small"
            # potentially hazardous objects < 50m burn up in atmosphere
            # 50m - 140m can cause localized ground damage

        elif diameter > 0.14 and diameter <= 0.5:
            score = self._interpolate(diameter, 0.14, 0.5, 5.0, 10.0)
            size = "medium"
            # capable of severe regional devastation

        elif diameter > 0.5 and diameter <= 1.0:
            score = self._interpolate(diameter, 0.5, 1.0, 10.0, 15.0)
            size = "large"
            # capable of multi-state or continental-scale disaster

        elif diameter > 1.0:
            score = self._interpolate(diameter, 1.0, 2.5, 15.0, 20.0)
            size = "giant"
            # global extinction threshold

        return (score, size)

    def _calc_velocity(self, record):
        velocity = record.relative_velocity_km_s
        if velocity < 12.0:
            score = self._interpolate(velocity, 0.0, 12.0, 0.0, 5.0)
            speed = "slow"

        elif velocity >= 12.0 and velocity < 20.0:
            score = self._interpolate(velocity, 12.0, 20.0, 5.0, 10.0)
            speed = "moderate"

        elif velocity >= 20.0 and velocity < 30.0:
            score = self._interpolate(velocity, 20.0, 30.0, 10.0, 15.0)
            speed = "fast"

        elif velocity >= 30.0:
            score = self._interpolate(velocity, 30.0, 50.0, 15.0, 20.0)
            speed = "very fast"

        return (score, speed)

    def _calc_distance(self, record):
        distance_km = record.miss_distance_km
        if distance_km < self.LUNAR_DISTANCE_KM:
            score = self._interpolate(
                distance_km, 0.0, self.LUNAR_DISTANCE_KM, 20.0, 15.0
            )
            distance = "extremely close"

        elif distance_km >= self.LUNAR_DISTANCE_KM and distance_km < (
            5 * self.LUNAR_DISTANCE_KM
        ):
            score = self._interpolate(
                distance_km,
                self.LUNAR_DISTANCE_KM,
                5 * self.LUNAR_DISTANCE_KM,
                15.0,
                10.0,
            )
            distance = "close"

        elif (
            distance_km >= (self.LUNAR_DISTANCE_KM * 5)
            and distance_km < self.NASA_PHA_KM
        ):
            score = self._interpolate(
                distance_km, 5 * self.LUNAR_DISTANCE_KM, self.NASA_PHA_KM, 10.0, 0.0
            )
            distance = "moderate"

        else:
            score = 0.0
            distance = "far"

        return (score, distance)

    def _calc_risk_level(self, total):
        if total <= 40:
            risk_level = "low"

        elif total > 40 and total < 71:
            risk_level = "moderate"

        elif total >= 71 and total < 91:
            risk_level = "high"

        elif total >= 91:
            risk_level = "extremely high"

        return risk_level

    def _interpolate(self, val, min_val, max_val, min_score, max_score):
        if val <= min_val:
            return min_score

        if val >= max_val:
            return max_score

        return min_score + (val - min_val) / (max_val - min_val) * (
            max_score - min_score
        )


""" 
score 1-100
low: 0 - 40, medium 41 - 70, high 71-90, extremely high 91-100

is_hazardous 40%
diameter 20%
distance 20%
velocity 20%
 """
