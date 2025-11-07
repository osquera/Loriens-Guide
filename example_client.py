#!/usr/bin/env python3
"""Example client script demonstrating how to use the Hafnia VLM API.

This script shows how a mobile app would interact with the backend server
to provide accessibility assistance to vision-impaired users.
"""

import requests


def main() -> None:
    """Run example API calls."""
    base_url = "http://localhost:5000"

    # Example 1: Health Check
    response = requests.get(f"{base_url}/health")

    # Example 2: List all cameras
    response = requests.get(f"{base_url}/api/v1/cameras")
    data = response.json()
    for _camera in data["cameras"]:
        pass

    # Example 3: Find nearest camera
    user_location = {"lat": 55.6761, "long": 12.5683}
    response = requests.post(f"{base_url}/api/v1/cameras/nearest", json=user_location)
    response.json()["camera"]

    # Example 4: Query the VLM (main use case)
    query_data = {"lat": 55.6761, "long": 12.5683, "question_text": "I'm looking for the exit, where is it?"}

    # Note: This will fail without a real VLM API key, but shows the flow
    response = requests.post(f"{base_url}/api/v1/query", json=query_data)

    result = response.json()

    if result.get("error"):
        pass

    # Example 5: Another query
    query_data = {"lat": 55.6763, "long": 12.5685, "question_text": "Where is the nearest bathroom?"}

    response = requests.post(f"{base_url}/api/v1/query", json=query_data)

    result = response.json()


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        pass
    except Exception:
        pass
