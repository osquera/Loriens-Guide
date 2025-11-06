#!/usr/bin/env python3
"""
Example client script demonstrating how to use the Hafnia VLM API.

This script shows how a mobile app would interact with the backend server
to provide accessibility assistance to vision-impaired users.
"""

import requests
import json


def main():
    """Run example API calls."""
    base_url = "http://localhost:5000"
    
    print("=" * 70)
    print("Lórien's Guide - Hafnia VLM API Demo")
    print("=" * 70)
    print()
    
    # Example 1: Health Check
    print("1. Health Check")
    print("-" * 70)
    response = requests.get(f"{base_url}/health")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Example 2: List all cameras
    print("2. List All Cameras")
    print("-" * 70)
    response = requests.get(f"{base_url}/api/v1/cameras")
    data = response.json()
    print(f"Total cameras: {len(data['cameras'])}")
    for camera in data['cameras']:
        print(f"  - {camera['camera_id']}: {camera['name']}")
    print()
    
    # Example 3: Find nearest camera
    print("3. Find Nearest Camera")
    print("-" * 70)
    user_location = {
        "lat": 55.6761,
        "long": 12.5683
    }
    print(f"User location: {user_location}")
    response = requests.post(
        f"{base_url}/api/v1/cameras/nearest",
        json=user_location
    )
    nearest = response.json()['camera']
    print(f"Nearest camera: {nearest['camera_id']} - {nearest['name']}")
    print(f"Video: {nearest['video_clip_url']}")
    print()
    
    # Example 4: Query the VLM (main use case)
    print("4. User Query - 'Where is the exit?'")
    print("-" * 70)
    query_data = {
        "lat": 55.6761,
        "long": 12.5683,
        "question_text": "I'm looking for the exit, where is it?"
    }
    print(f"User question: {query_data['question_text']}")
    print(f"User location: ({query_data['lat']}, {query_data['long']})")
    print()
    
    # Note: This will fail without a real VLM API key, but shows the flow
    print("Making API call...")
    response = requests.post(
        f"{base_url}/api/v1/query",
        json=query_data
    )
    
    result = response.json()
    print("Response:")
    print(f"  Camera: {result.get('camera_name', 'N/A')}")
    print(f"  Answer: {result.get('answer', result.get('message', 'N/A'))}")
    
    if result.get('error'):
        print(f"  Note: Error occurred (expected without VLM API key)")
    print()
    
    # Example 5: Another query
    print("5. User Query - 'Where is the bathroom?'")
    print("-" * 70)
    query_data = {
        "lat": 55.6763,
        "long": 12.5685,
        "question_text": "Where is the nearest bathroom?"
    }
    print(f"User question: {query_data['question_text']}")
    print(f"User location: ({query_data['lat']}, {query_data['long']})")
    print()
    
    response = requests.post(
        f"{base_url}/api/v1/query",
        json=query_data
    )
    
    result = response.json()
    print("Response:")
    print(f"  Camera: {result.get('camera_name', 'N/A')}")
    print(f"  Answer: {result.get('answer', result.get('message', 'N/A'))}")
    print()
    
    print("=" * 70)
    print("Demo Complete!")
    print()
    print("To use with a real VLM API:")
    print("1. Set VLM_API_KEY in .env file")
    print("2. Set VLM_API_URL to your VLM endpoint")
    print("3. Restart the server")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")
        print("Please make sure the server is running:")
        print("  python app.py")
    except Exception as e:
        print(f"Error: {e}")
