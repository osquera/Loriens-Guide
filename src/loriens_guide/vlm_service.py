"""VLM Service Module.

Handles the core logic for:
1. Finding the nearest camera based on user location
2. Constructing prompts for the VLM API
3. Calling the Hafnia VLM API
"""

import json
import logging
import math
import os
from pathlib import Path

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VLMService:
    """Service for handling VLM API interactions and camera management."""

    def __init__(self, cameras_file: str = "cameras.json") -> None:
        """Initialize the VLM service.

        Args:
            cameras_file: Path to the cameras.json configuration file

        """
        self.cameras_file = Path(cameras_file)
        self.cameras = self._load_cameras()
        # Milestone Hackathon API Configuration
        base_url = os.getenv("VLM_API_URL", "https://api.mdi.milestonesys.com")
        # Normalize base URL by removing trailing /api/v1 or trailing slash
        self.vlm_api_base = base_url.removesuffix("/api/v1").removesuffix("/")
        self.api_key = os.getenv("HACKATHON_API_KEY", "")
        self.api_secret = os.getenv("HACKATHON_API_SECRET", "")

    def _load_cameras(self) -> list:
        """Load camera data from JSON file.

        Returns:
            List of camera dictionaries

        """
        try:
            with Path.open(self.cameras_file) as f:
                data = json.load(f)
                return data.get("cameras", [])
        except FileNotFoundError:
            logger.warning(f"Warning: {self.cameras_file} not found")
            return []
        except json.JSONDecodeError:
            logger.exception(f"Error parsing {self.cameras_file}")
            return []

    def _calculate_distance(self, lat1: float, long1: float, lat2: float, long2: float) -> float:
        """Calculate the distance between two coordinates using Haversine formula.

        Args:
            lat1: Latitude of first point
            long1: Longitude of first point
            lat2: Latitude of second point
            long2: Longitude of second point

        Returns:
            Distance in meters

        """
        # Earth's radius in meters
        R = 6371000  # noqa: N806

        # Convert to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_long = math.radians(long2 - long1)

        # Haversine formula
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_long / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def find_nearest_camera(self, lat: float, long: float) -> dict | None:
        """Find the camera nearest to the given coordinates.

        Args:
            lat: User's latitude
            long: User's longitude

        Returns:
            Dictionary containing the nearest camera's data, or None if no cameras available

        """
        if not self.cameras:
            return None

        nearest_camera = None
        min_distance = float("inf")

        for camera in self.cameras:
            camera_lat = camera["location"]["lat"]
            camera_long = camera["location"]["long"]

            distance = self._calculate_distance(lat, long, camera_lat, camera_long)

            if distance < min_distance:
                min_distance = distance
                nearest_camera = camera

        return nearest_camera

    def _construct_vlm_prompt(self, question_text: str, context_description: str) -> str:
        """Construct the prompt to send to the VLM API.

        This is the core of the submission - the prompt crafting is critical.

        Args:
            question_text: The user's question
            context_description: Description of the camera location and orientation

        Returns:
            Formatted prompt string for the VLM API

        """
        return (
            f"You are an accessibility assistant for a user with vision impairment. "
            f"The user is at the '{context_description}'.\n\n"
            f"They have asked: '{question_text}'\n\n"
            f"Analyze the attached video clip of this location. "
            f"Provide a safe, clear, and direct answer. "
            f"Use landmarks and steps (e.g., 'on your left,' 'walk 10 steps'), not colors."
        )

    def upload_video_asset(self, video_path: str) -> dict:
        """Upload a video asset to the Milestone Hackathon API.

        Args:
            video_path: Path to the video file (.mp4 or .mkv, <100MB, <30s)

        Returns:
            Dictionary with asset_id or error information

        """
        upload_url = f"{self.vlm_api_base}/api/v1/assets"
        auth_header = f"ApiKey {self.api_key}:{self.api_secret}"
        headers = {"Authorization": auth_header}

        try:
            with open(video_path, "rb") as video_file:
                files = {"file": video_file}
                response = requests.post(upload_url, headers=headers, files=files, timeout=120)

            # Accept both 200 OK and 201 Created as success
            if response.status_code in (requests.codes.ok, requests.codes.created):
                data = response.json()
                # The API returns "id" field, but we need "asset_id" for consistency
                if "id" in data and "asset_id" not in data:
                    data["asset_id"] = data["id"]
                return data
            logger.error(f"Asset upload failed: {response.status_code} - {response.text}")

        except Exception as e:
            logger.exception("Failed to upload video asset")
            return {"error": True, "message": f"Upload exception: {e!s}"}
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": f"Asset upload failed: {response.status_code}",
            }

    def call_vlm_api(self, asset_id: str, user_prompt: str, system_prompt: str | None = None) -> dict:
        """Call the Milestone Hackathon VLM API with asset and prompts.

        Args:
            asset_id: The asset_id returned from upload_video_asset()
            user_prompt: The user's question/request text
            system_prompt: Optional system prompt for output format/safety

        Returns:
            Dictionary containing the VLM response

        """
        chat_url = f"{self.vlm_api_base}/api/v1/chat/completions"
        auth_header = f"ApiKey {self.api_key}:{self.api_secret}"
        headers = {"Authorization": auth_header, "Content-Type": "application/json"}

        # Build messages array per Hackathon API spec
        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": [{"type": "text", "text": system_prompt}]})

        # Add user message with text and asset reference
        messages.append(
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}, {"type": "asset_id", "asset_id": asset_id}],
            }
        )

        payload = {"messages": messages}

        try:
            response = requests.post(chat_url, json=payload, headers=headers, timeout=180)

            if response.status_code == requests.codes.ok:
                result = response.json()
                # Extract the text response from OpenAI-style format
                if "choices" in result and len(result["choices"]) > 0:
                    text_response = result["choices"][0].get("message", {}).get("content", "")
                    return {"text": text_response, "full_response": result}
                return result
            logger.error(f"VLM API error: {response.status_code} - {response.text}")

        except requests.exceptions.Timeout:
            logger.exception("VLM API request timed out")
            return {
                "error": True,
                "message": "VLM API request timed out after 180 seconds",
                "text": "I'm sorry, the video analysis took too long. Please try again with a shorter clip.",
            }
        except requests.exceptions.RequestException:
            logger.exception("Failed to connect to VLM API")
            return {
                "error": True,
                "message": "Failed to connect to VLM API",
                "text": "I'm sorry, I'm having trouble connecting to the vision service. Please try again.",
            }
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": f"VLM API returned status code {response.status_code}",
                "text": "I'm sorry, I couldn't analyze the video at this time. Please try again.",
            }

    def delete_asset(self, asset_id: str) -> bool:
        """Delete a video asset from the Milestone API.

        Args:
            asset_id: The asset_id to delete

        Returns:
            True if successful, False otherwise

        """
        delete_url = f"{self.vlm_api_base}/api/v1/assets/{asset_id}"
        auth_header = f"ApiKey {self.api_key}:{self.api_secret}"
        headers = {"Authorization": auth_header}

        try:
            response = requests.delete(delete_url, headers=headers, timeout=60)

        except Exception:
            logger.exception(f"Failed to delete asset {asset_id}")
            return False
        return response.status_code in (requests.codes.ok, requests.codes.no_content)

    def process_user_request(self, lat: float, long: float, question_text: str) -> dict:
        """Process a complete user request end-to-end.

        This is the main method that orchestrates the entire flow:
        1. Find nearest camera
        2. Get video & context
        3. Call Hafnia VLM
        4. Return response

        Args:
            lat: User's latitude
            long: User's longitude
            question_text: The user's question

        Returns:
            Dictionary with the response to send back to the user

        """
        # Step 1: Find nearest camera
        nearest_camera = self.find_nearest_camera(lat, long)

        if not nearest_camera:
            return {
                "error": True,
                "message": "No cameras available in your area",
                "text": "I'm sorry, there are no cameras available in your area.",
            }

        # Step 2: Get video & context
        video_clip_url = nearest_camera["video_clip_url"]
        context_description = nearest_camera["context_description"]
        camera_id = nearest_camera["camera_id"]

        # Step 3: Construct prompt
        prompt = self._construct_vlm_prompt(question_text, context_description)

        # Step 4: Call Hafnia VLM
        vlm_response = self.call_vlm_api(video_clip_url, prompt)

        # Step 5: Format response for mobile app
        return {
            "camera_id": camera_id,
            "camera_name": nearest_camera["name"],
            "question": question_text,
            "answer": vlm_response.get("text", ""),
            "error": vlm_response.get("error", False),
        }
