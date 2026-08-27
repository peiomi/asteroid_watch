import requests

# store secrets in google cloud secrets manager
NASA_URL = "NASA.REAL.COM"
# cloud scheduler is the trigger

# IAM roles: ETL service acct, Bot service acct, Scheduler service acct


class PsuedoCode:
    def __init__(
        self,
        plan,
    ):
        self.plan = plan

    # create storage bucket for raw json/error logs
    def store_in_bucket(self, raw_json, errors):
        print(f"storing: {raw_json} & {errors}")

    # ingestion service gets triggered, fetches, processes, and stores data
    def on_trigger(self):
        raw_json = self.fetch_from_nasa()
        self.store_in_bucket(raw_json)
        records = self.normalize(raw_json)
        scored_records = self.add_risk_scores(records)
        self.write_to_database(scored_records)

    # NASA API responds with data
    def fetch_from_nasa(self):
        response = requests.get(NASA_URL, params={}, timeout=69)
        return response.json()

    def normalize(self, raw_json):
        print(raw_json)
        return

    def add_risk_scores(self, records):
        return records.result1 + records.result2

    def write_to_database(self, scored_records):
        self.post(scored_records)

    # analytics produces insights of the data ex: "average risk score for last 24 hrs"
    def on_analytics_request(self):
        records = self.query_database()
        insights = self.average_risk_score(records)
        return self.insights_to_client(insights)

    # model:
    def record_model():
        id = "unique identifier"  # string
        name = "label"  # string
        diameter_min = "estimated_diameter.kilometers.estimated_diameter_min"  # float
        diameter_max = "estimated_diameter.kilometers.estimated_diameter_max"  # float
        # need min/max bc size is a major risk factor
        miss_distance_km = "close_approach_data[0].miss_distance.kilometers"  # float
        relative_velocity_km_s = (
            "close_approach_data[0].relative_velocity.kilometers_per_second"  # float
        )
        is_hazardous = "is_potentially_hazardous_asteroid"  # bool
        close_approach_date = "close_approach_data[0].close_approach_date"  # date
        risk_score = (
            "what i am trying to calculate from the data i am receiving"  # float or int
        )


""" 
ideas:
- a bot that posts info every 6 hours or 1x a day with a photo on bluesky/twitter 
- add a cloud run analytics API
- monitoring dashboard, function latency, error rate 
- Terraform

"""
