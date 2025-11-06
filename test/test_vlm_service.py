"""Unit tests for VLM Service."""

import unittest
from unittest.mock import MagicMock, patch

from src.loriens_guide.vlm_service import VLMService


class TestVLMService(unittest.TestCase):
    """Test cases for VLMService class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.service = VLMService()

    def test_calculate_distance(self) -> None:
        """Test distance calculation between two coordinates."""
        # Copenhagen coordinates (approximately 500m apart)
        lat1, long1 = 55.6761, 12.5683
        lat2, long2 = 55.6800, 12.5683

        distance = self.service._calculate_distance(lat1, long1, lat2, long2)  # noqa: SLF001

        # Should be approximately 433 meters
        self.assertGreater(distance, 400)
        self.assertLess(distance, 500)

    def test_calculate_distance_same_point(self) -> None:
        """Test distance calculation for the same point."""
        lat, long = 55.6761, 12.5683

        distance = self.service._calculate_distance(lat, long, lat, long)  # noqa: SLF001

        self.assertEqual(distance, 0)

    def test_find_nearest_camera(self) -> None:
        """Test finding the nearest camera to user location."""
        # Location very close to lib_lobby_01
        lat, long = 55.6761, 12.5683

        nearest = self.service.find_nearest_camera(lat, long)

        self.assertIsNotNone(nearest)
        self.assertEqual(nearest["camera_id"], "lib_lobby_01") # pyright: ignore[reportOptionalSubscript]

    def test_find_nearest_camera_different_location(self) -> None:
        """Test finding nearest camera from a different location."""
        # Location closer to lib_exit_01
        lat, long = 55.6759, 12.5681

        nearest = self.service.find_nearest_camera(lat, long)

        self.assertIsNotNone(nearest)
        self.assertEqual(nearest["camera_id"], "lib_exit_01") # pyright: ignore[reportOptionalSubscript]

    def test_construct_vlm_prompt(self) -> None:
        """Test VLM prompt construction."""
        question = "Where is the exit?"
        context = "Library Lobby - Main Entrance, facing east"

        prompt = self.service._construct_vlm_prompt(question, context)  # noqa: SLF001

        # Check key elements are in prompt
        self.assertIn("accessibility assistant", prompt)
        self.assertIn("vision impairment", prompt)
        self.assertIn(question, prompt)
        self.assertIn(context, prompt)
        self.assertIn("landmarks and steps", prompt)
        self.assertIn("not colors", prompt)

    @patch("vlm_service.requests.post")
    def test_call_vlm_api_success(self, mock_post: MagicMock) -> None:
        """Test successful VLM API call."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": "The exit is 20 steps forward."}
        mock_post.return_value = mock_response

        result = self.service.call_vlm_api("videos/test.mp4", "Test prompt")

        self.assertFalse(result.get("error", False))
        self.assertEqual(result["text"], "The exit is 20 steps forward.")

    @patch("vlm_service.requests.post")
    def test_call_vlm_api_error(self, mock_post: MagicMock) -> None:
        """Test VLM API call with error response."""
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = self.service.call_vlm_api("videos/test.mp4", "Test prompt")

        self.assertTrue(result.get("error", False))
        self.assertIn("text", result)

    @patch("vlm_service.requests.post")
    def test_process_user_request(self, mock_post: MagicMock) -> None:
        """Test complete user request processing."""
        # Mock successful VLM response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": "Walk straight ahead for 15 steps. The bathroom is on your left."}
        mock_post.return_value = mock_response

        # Process request
        result = self.service.process_user_request(lat=55.6761, long=12.5683, question_text="Where is the bathroom?")

        # Verify response structure
        self.assertIn("camera_id", result)
        self.assertIn("camera_name", result)
        self.assertIn("question", result)
        self.assertIn("answer", result)
        self.assertEqual(result["question"], "Where is the bathroom?")
        self.assertFalse(result.get("error", False))


if __name__ == "__main__":
    unittest.main()
