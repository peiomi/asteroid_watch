import unittest
from src.etl.risk_scorer import RiskScorer
from tests.mock_records import MOCK_RECORDS


class TestRiskScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = RiskScorer()

    def test_score_risk_returns_risk_scores(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        self.assertEqual(len(results), len(MOCK_RECORDS))

    def test_extremely_high_risk(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        extreme = results[3]

        self.assertEqual(extreme.id, "4")
        self.assertEqual(extreme.name, "Apocalypse Andy")
        self.assertEqual(extreme.size, "giant")
        self.assertEqual(extreme.speed, "very fast")
        self.assertEqual(extreme.distance, "extremely close")
        self.assertEqual(extreme.risk_score, 100)
        self.assertEqual(extreme.risk_level, "extremely high")

    def test_high_risk(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        high = results[2]
        self.assertEqual(high.id, "3")
        self.assertEqual(high.name, "Danger Dave")
        self.assertEqual(high.size, "large")
        self.assertEqual(high.speed, "fast")
        self.assertEqual(high.distance, "close")
        self.assertEqual(high.risk_score, 85)
        self.assertEqual(high.risk_level, "high")

    def test_medium_risk(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        medium = results[1]
        self.assertEqual(medium.id, "2")
        self.assertEqual(medium.name, "Medium Mike")
        self.assertEqual(medium.size, "medium")
        self.assertEqual(medium.speed, "moderate")
        self.assertEqual(medium.distance, "moderate")
        self.assertEqual(medium.risk_score, 70)
        self.assertEqual(medium.risk_level, "moderate")

    def test_low_risk(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        low = results[0]
        self.assertEqual(low.id, "1")
        self.assertEqual(low.name, "Tiny Tim")
        self.assertEqual(low.size, "small")
        self.assertEqual(low.speed, "slow")
        self.assertEqual(low.distance, "far")
        self.assertEqual(low.risk_score, 15)
        self.assertEqual(low.risk_level, "low")

    def test_hazardous_calc(self):
        score = self.scorer._calc_hazard(MOCK_RECORDS[3])
        self.assertEqual(score, 40)

    def test_non_hazardous_calc(self):
        score = self.scorer._calc_hazard(MOCK_RECORDS[0])
        self.assertEqual(score, 0)

    def test_size_calc(self):
        small_score, small_size = self.scorer._calc_size(MOCK_RECORDS[0])
        self.assertEqual(small_score, 5)
        self.assertEqual(small_size, "small")

        medium_score, medium_size = self.scorer._calc_size(MOCK_RECORDS[1])
        self.assertEqual(medium_score, 10)
        self.assertEqual(medium_size, "medium")

        large_score, large_size = self.scorer._calc_size(MOCK_RECORDS[2])
        self.assertEqual(large_score, 15)
        self.assertEqual(large_size, "large")

        giant_score, giant_size = self.scorer._calc_size(MOCK_RECORDS[3])
        self.assertEqual(giant_score, 20)
        self.assertEqual(giant_size, "giant")


if __name__ == "__main__":
    unittest.main()
