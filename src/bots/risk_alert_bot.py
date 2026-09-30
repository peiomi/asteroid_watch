class RiskAlertBot:
    def __init__(self, scored_asteroids):
        self.asteroids = scored_asteroids

    def find_highest_risk(self):
        highest = max(self.asteroids, key=lambda a: a.risk_score, default=None)
        return highest

    def find_average_risk(self):
        if not self.asteroids:
            return 0

        average = sum(a.risk_score for a in self.asteroids) / len(self.asteroids)

        return average

    def generate_post(self):
        asteroid = self.find_highest_risk()
        average = self.find_average_risk()

        if asteroid is None:
            return "No asteroid data available."

        return (
            f"🚨 Asteroid Watch Alert 🚨\n"
            f"Object: {asteroid.name}\n"
            f"Risk Score: {asteroid.risk_score:.2f}\n"
            f"Risk Level: {asteroid.risk_level}\n"
            f"Average Risk Score Today: {average}\n"
            "Source: NASA NEO API"
        )
