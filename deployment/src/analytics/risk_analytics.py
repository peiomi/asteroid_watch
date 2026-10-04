from google.cloud import bigquery
from src.etl.settings import Settings


class RiskAnalytics:
    def __init__(self):
        self.client = bigquery.Client()

    def get_highest_risk(self):
        query = f"""
        SELECT name, risk_score, risk_level, size, speed, distance
        FROM {Settings.RISK_TABLE}
        WHERE DATE(processed_at) = CURRENT_DATE()
        ORDER BY risk_score DESC
        LIMIT 1
        """

        rows = list(self.client.query(query).result())

        return rows[0] if rows else None

    def get_average_risk(self):
        query = f"""
        SELECT AVG(risk_score) AS average_risk
        FROM {Settings.RISK_TABLE}
        WHERE DATE(processed_at) = CURRENT_DATE()
        """

        rows = list(self.client.query(query).result())

        return rows[0].average_risk if rows else 0

    def get_risk_breakdown(self):
        query = f"""
        SELECT risk_level, COUNT(*) AS asteroid_count
        FROM {Settings.RISK_TABLE}
        WHERE DATE(processed_at) = CURRENT_DATE()
        GROUP BY risk_level
        ORDER BY asteroid_count DESC
        """

        return list(self.client.query(query).result())

    def get_hazardous_count(self):
        query = f"""
        SELECT COUNT(*) AS hazardous_count
        FROM {Settings.ASTEROID_TABLE}
        WHERE is_hazardous = TRUE
        AND DATE(processed_at) = CURRENT_DATE()
        """

        rows = list(self.client.query(query).result())

        return rows[0].hazardous_count if rows else 0
