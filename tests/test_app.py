import unittest

from app import calculate_demo_index, create_app


class DemoApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_demo_index_returns_clear_non_predictive_notice(self):
        response = self.client.post(
            "/predict",
            json={
                "age": 35,
                "distance_km": 10,
                "physical_ability": 5,
                "dose_rate_usv_h": 0,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["demo_index"], 20.0)
        self.assertIn("not a survival probability", response.get_json()["notice"])
        self.assertNotIn("prediction", response.get_json())

    def test_demo_index_uses_all_four_inputs(self):
        baseline = calculate_demo_index(35, 10, 5, 0)
        changed = calculate_demo_index(40, 20, 6, 1000)

        self.assertNotEqual(baseline, changed)

    def test_predict_rejects_missing_extra_or_invalid_fields(self):
        valid = {
            "age": 35,
            "distance_km": 10,
            "physical_ability": 5,
            "dose_rate_usv_h": 0,
        }
        invalid_payloads = (
            {},
            {**valid, "unexpected": 1},
            {**valid, "age": True},
            {**valid, "age": 121},
            {**valid, "distance_km": -1},
            {**valid, "physical_ability": 11},
            {**valid, "dose_rate_usv_h": float("inf")},
            {**valid, "dose_rate_usv_h": 1_000_001},
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post("/predict", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_predict_requires_json_content_type(self):
        response = self.client.post("/predict", data="age=35")

        self.assertEqual(response.status_code, 415)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
