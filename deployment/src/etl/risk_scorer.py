from src.etl.models import RiskScore

# will figure out exact math this is just placeholder math


class RiskScorer:
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

            score = RiskScore(
                id=record.id,
                name=record.name,
                size=size_score[1],
                speed=velocity_score[1],
                distance=distance_score[1],
                risk_score=total,
                risk_level=self._calc_risk_level(total),
            )
            risk_scores.append(score)

        return risk_scores

    def _calc_hazard(self, record):
        if record.is_hazardous:
            return 40
        return 0

    def _calc_size(self, record):
        diameter = (record.diameter_min + record.diameter_max) / 2
        if diameter <= 0.1:
            score = 5
            size = "small"
        elif diameter > 0.1 and diameter <= 0.5:
            score = 10
            size = "medium"
        elif diameter > 0.5 and diameter <= 1.0:
            score = 15
            size = "large"
        elif diameter > 1.0:
            score = 20
            size = "giant"
        return (score, size)

    def _calc_velocity(self, record):
        velocity = record.relative_velocity_km_s
        if velocity < 10.0:
            score = 5
            speed = "slow"
        elif velocity >= 10.0 and velocity < 20.0:
            score = 10
            speed = "moderate"
        elif velocity >= 20.0 and velocity < 30.0:
            score = 15
            speed = "fast"
        elif velocity >= 30.0:
            score = 20
            speed = "very fast"
        return (score, speed)

    def _calc_distance(self, record):
        distance_km = record.miss_distance_km
        if distance_km < 1_000_000.0:
            score = 20
            distance = "extremely close"
        elif distance_km >= 1_000_000.0 and distance_km < 5_000_000.0:
            score = 15
            distance = "close"
        elif distance_km >= 5_000_000.0 and distance_km < 20_000_000.0:
            score = 10
            distance = "moderate"
        elif distance_km >= 20_000_000.0:
            score = 5
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


""" 
score 1-100
low: 0 - 40, medium 41 - 70, high 71-90, extremely high 91-100

is_hazardous 40%
diameter 20%
distance 20%
velocity 20%
 """
