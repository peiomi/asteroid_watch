import unittest
from deployment.src.etl.risk_scorer import RiskScorer
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
        self.assertAlmostEqual(extreme.risk_score, 93.74, places=2)
        self.assertEqual(extreme.risk_level, "extremely high")

    def test_high_risk(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        high = results[2]
        self.assertEqual(high.id, "3")
        self.assertEqual(high.name, "Danger Dave")
        self.assertEqual(high.size, "large")
        self.assertEqual(high.speed, "fast")
        self.assertEqual(high.distance, "moderate")
        self.assertAlmostEqual(high.risk_score, 76.11, places=2)
        self.assertEqual(high.risk_level, "high")

    def test_medium_risk(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        medium = results[1]

        self.assertEqual(medium.id, "2")
        self.assertEqual(medium.name, "Medium Mike")
        self.assertEqual(medium.size, "medium")
        self.assertEqual(medium.speed, "moderate")
        self.assertEqual(medium.distance, "far")
        self.assertAlmostEqual(medium.risk_score, 55.14, places=2)
        self.assertEqual(medium.risk_level, "moderate")

    def test_low_risk(self):
        results = self.scorer.score_risk(MOCK_RECORDS)
        low = results[0]

        self.assertEqual(low.id, "1")
        self.assertEqual(low.name, "Tiny Tim")
        self.assertEqual(low.size, "small")
        self.assertEqual(low.speed, "slow")
        self.assertEqual(low.distance, "far")
        self.assertAlmostEqual(low.risk_score, 4.76, places=2)
        self.assertEqual(low.risk_level, "low")

    def test_hazardous_calc(self):
        score = self.scorer._calc_hazard(MOCK_RECORDS[3])
        self.assertEqual(score, 40)

    def test_non_hazardous_calc(self):
        score = self.scorer._calc_hazard(MOCK_RECORDS[0])
        self.assertEqual(score, 0)

    def test_size_calc(self):
        small_score, small_size = self.scorer._calc_size(MOCK_RECORDS[0])
        self.assertAlmostEqual(small_score, 2.68, places=2)
        self.assertEqual(small_size, "small")

        medium_score, medium_size = self.scorer._calc_size(MOCK_RECORDS[1])
        self.assertAlmostEqual(medium_score, 8.26, places=2)
        self.assertEqual(medium_size, "medium")

        large_score, large_size = self.scorer._calc_size(MOCK_RECORDS[2])
        self.assertAlmostEqual(large_score, 13.75, places=2)
        self.assertEqual(large_size, "large")

        giant_score, giant_size = self.scorer._calc_size(MOCK_RECORDS[3])
        self.assertAlmostEqual(giant_score, 17.50, places=2)
        self.assertEqual(giant_size, "giant")


if __name__ == "__main__":
    unittest.main()
