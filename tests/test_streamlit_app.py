import unittest
from unittest.mock import Mock, patch

import requests

from streamlit_app import request_demo_index


class StreamlitDemoTests(unittest.TestCase):
    @patch("streamlit_app.requests.post")
    def test_request_sends_named_inputs_and_returns_demo_index(self, post):
        response = Mock()
        response.json.return_value = {"demo_index": 39.8}
        post.return_value = response
        inputs = {
            "age": 35,
            "distance_km": 10,
            "physical_ability": 5,
            "dose_rate_usv_h": 0,
        }

        result = request_demo_index("http://localhost:5000/", inputs)

        self.assertEqual(result, 39.8)
        post.assert_called_once_with(
            "http://localhost:5000/predict",
            json=inputs,
            timeout=(3, 30),
        )
        response.raise_for_status.assert_called_once_with()

    @patch("streamlit_app.requests.post")
    def test_request_rejects_invalid_demo_index(self, post):
        response = Mock()
        response.json.return_value = {"demo_index": "high"}
        post.return_value = response

        with self.assertRaisesRegex(ValueError, "valid demo index"):
            request_demo_index("http://localhost:5000", {})

    @patch("streamlit_app.requests.post")
    def test_request_propagates_http_errors(self, post):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("bad request")
        post.return_value = response

        with self.assertRaises(requests.HTTPError):
            request_demo_index("http://localhost:5000", {})


if __name__ == "__main__":
    unittest.main()
