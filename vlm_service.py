"""
VLM Service Module

Handles the core logic for:
1. Finding the nearest camera based on user location
2. Constructing prompts for the VLM API
3. Calling the Hafnia VLM API
"""

import json
import logging
import math
import os
from typing import Dict, Optional, Tuple
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VLMService:
    """Service for handling VLM API interactions and camera management."""
    
    def __init__(self, cameras_file: str = "cameras.json"):
        """Initialize the VLM service.
        
        Args:
            cameras_file: Path to the cameras.json configuration file
        """
        self.cameras_file = cameras_file
        self.cameras = self._load_cameras()
        self.vlm_api_url = os.getenv("VLM_API_URL", "https://api.hafnia.ai/v1/vlm")
        self.vlm_api_key = os.getenv("VLM_API_KEY", "")
    
    def _load_cameras(self) -> list:
        """Load camera data from JSON file.
        
        Returns:
            List of camera dictionaries
        """
        try:
            with open(self.cameras_file, 'r') as f:
                data = json.load(f)
                return data.get('cameras', [])
        except FileNotFoundError:
            logger.warning(f"Warning: {self.cameras_file} not found")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing {self.cameras_file}: {e}")
            return []
    
    def _calculate_distance(self, lat1: float, long1: float, 
                           lat2: float, long2: float) -> float:
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
        R = 6371000
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_long = math.radians(long2 - long1)
        
        # Haversine formula
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_long / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def find_nearest_camera(self, lat: float, long: float) -> Optional[Dict]:
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
        min_distance = float('inf')
        
        for camera in self.cameras:
            camera_lat = camera['location']['lat']
            camera_long = camera['location']['long']
            
            distance = self._calculate_distance(lat, long, camera_lat, camera_long)
            
            if distance < min_distance:
                min_distance = distance
                nearest_camera = camera
        
        return nearest_camera
    
    def _construct_vlm_prompt(self, question_text: str, 
                             context_description: str) -> str:
        """Construct the prompt to send to the VLM API.
        
        This is the core of the submission - the prompt crafting is critical.
        
        Args:
            question_text: The user's question
            context_description: Description of the camera location and orientation
            
        Returns:
            Formatted prompt string for the VLM API
        """
        prompt = (
            f"You are an accessibility assistant for a user with vision impairment. "
            f"The user is at the '{context_description}'.\n\n"
            f"They have asked: '{question_text}'\n\n"
            f"Analyze the attached video clip of this location. "
            f"Provide a safe, clear, and direct answer. "
            f"Use landmarks and steps (e.g., 'on your left,' 'walk 10 steps'), not colors."
        )
        return prompt
    
    def call_vlm_api(self, video_clip_url: str, prompt: str) -> Dict:
        """Call the Hafnia VLM API with video and prompt.
        
        Args:
            video_clip_url: URL or path to the video clip
            prompt: The constructed prompt for the VLM
            
        Returns:
            Dictionary containing the VLM response
        """
        # Prepare the request payload
        payload = {
            "video_url": video_clip_url,
            "prompt": prompt,
            "max_tokens": 500
        }
        
        headers = {
            "Authorization": f"Bearer {self.vlm_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                self.vlm_api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                # Return error information
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": f"VLM API returned status code {response.status_code}",
                    "text": "I'm sorry, I couldn't analyze the video at this time. Please try again."
                }
        except requests.exceptions.RequestException:
            # Handle network errors - don't expose details
            logger.error("Failed to connect to VLM API")
            return {
                "error": True,
                "message": "Failed to connect to VLM API",
                "text": "I'm sorry, I'm having trouble connecting to the vision service. Please try again."
            }
    
    def process_user_request(self, lat: float, long: float, 
                            question_text: str) -> Dict:
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
                "text": "I'm sorry, there are no cameras available in your area."
            }
        
        # Step 2: Get video & context
        video_clip_url = nearest_camera['video_clip_url']
        context_description = nearest_camera['context_description']
        camera_id = nearest_camera['camera_id']
        
        # Step 3: Construct prompt
        prompt = self._construct_vlm_prompt(question_text, context_description)
        
        # Step 4: Call Hafnia VLM
        vlm_response = self.call_vlm_api(video_clip_url, prompt)
        
        # Step 5: Format response for mobile app
        response = {
            "camera_id": camera_id,
            "camera_name": nearest_camera['name'],
            "question": question_text,
            "answer": vlm_response.get("text", ""),
            "error": vlm_response.get("error", False)
        }
        
        return response
