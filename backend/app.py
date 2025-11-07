"""Lórien's Guide - Backend Orchestrator.

A lightweight server to handle logic for vision-impaired assistance in public spaces.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load camera registry
CAMERA_REGISTRY_PATH = Path(__file__).parent / "camera_registry.json"


def load_camera_registry() -> dict:
    """Load the camera registry from JSON file."""
    try:
        with CAMERA_REGISTRY_PATH.open() as f:
            return json.load(f)
    except FileNotFoundError:
        return {"cameras": []}


def save_camera_registry(registry: dict) -> None:
    """Save the camera registry to JSON file."""
    with CAMERA_REGISTRY_PATH.open("w") as f:
        json.dump(registry, f, indent=2)


@app.route("/api/health", methods=["GET"])
def health_check() -> Response:
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Lórien's Guide Backend"})


@app.route("/api/cameras", methods=["GET"])
def get_cameras() -> Response:
    """Get all cameras from the registry."""
    registry = load_camera_registry()
    return jsonify(registry)


@app.route("/api/cameras/<camera_id>", methods=["GET"])
def get_camera(camera_id: str) -> Response | tuple[Response, int]:
    """Get a specific camera by ID."""
    registry = load_camera_registry()
    for camera in registry.get("cameras", []):
        if camera["id"] == camera_id:
            return jsonify(camera)
    return jsonify({"error": "Camera not found"}), 404


@app.route("/api/cameras/nearby", methods=["POST"])
def get_nearby_cameras() -> tuple[Response, Literal[400]] | Response:
    """Get cameras near a specific location."""
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON payload"}), 400
    lat = data.get("latitude")
    lon = data.get("longitude")
    _radius = data.get("radius", 100)  # Default radius in meters

    if lat is None or lon is None:
        return jsonify({"error": "Latitude and longitude required"}), 400

    registry = load_camera_registry()
    # Simple distance calculation (for hackathon purposes)
    # Keep only cameras that have a location (replace loop with list comprehension)
    nearby_cameras = [camera for camera in registry.get("cameras", []) if camera.get("location")]

    return jsonify({"cameras": nearby_cameras})


@app.route("/api/vlm/analyze", methods=["POST"])
def analyze_with_vlm() -> tuple[Response, Literal[400]] | Response:
    """Endpoint to analyze camera feed with Hafnia VLM.

    This is a placeholder for VLM integration.
    """
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON payload"}), 400
    camera_id = data.get("camera_id")
    query = data.get("query", "Describe what you see")

    if not camera_id:
        return jsonify({"error": "Camera ID required"}), 400

    # Placeholder response - integrate with actual Hafnia VLM API
    response = {
        "camera_id": camera_id,
        "query": query,
        "analysis": "VLM integration placeholder - describe the scene from camera feed",
        "confidence": 0.85,
        "timestamp": datetime.now(tz=datetime.now().astimezone().tzinfo).isoformat(),
    }

    return jsonify(response)


@app.route("/api/voice/transcribe", methods=["POST"])
def transcribe_audio() -> Response:
    """Endpoint for Speech-to-Text processing.

    This is a placeholder for STT integration.
    """
    # In real implementation, process audio data
    # For now, return a mock response
    return jsonify({"text": "Mock transcription - integrate with STT service", "confidence": 0.9})


@app.route("/api/voice/synthesize", methods=["POST"])
def synthesize_speech() -> tuple[Response, Literal[400]] | Response:
    """Endpoint for Text-to-Speech processing.

    This is a placeholder for TTS integration.
    """
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON payload"}), 400
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text required"}), 400

    # Placeholder response - integrate with actual TTS service
    return jsonify(
        {
            "audio_url": "/mock/audio.mp3",
            "text": text,
            "duration": len(text) * 0.1,  # Mock duration
        }
    )


@app.route("/api/assistance/request", methods=["POST"])
def request_assistance() -> tuple[Response, Literal[400]] | Response:
    """Endpoint for requesting assistance.

    Combines camera lookup, VLM analysis, and voice response.
    """
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON payload"}), 400
    location = data.get("location")
    _query = data.get("query", "What do you see?")

    if not location:
        return jsonify({"error": "Location required"}), 400

    # Get nearby cameras
    registry = load_camera_registry()
    cameras = registry.get("cameras", [])

    if not cameras:
        return jsonify({"message": "No cameras available in this area", "cameras": []})

    # Use first available camera (simplified for hackathon)
    camera = cameras[0] if cameras else None

    if camera:
        # Simulate VLM analysis
        response = {
            "camera": camera,
            "analysis": f"Analysis from camera {camera['id']}: {camera.get('description', 'Scene description')}",
            "voice_response": f"I can see {camera.get('description', 'the area around you')}",
            "timestamp": datetime.now(tz=datetime.now().astimezone().tzinfo).isoformat(),
        }
    else:
        response = {"message": "No cameras available", "voice_response": "Sorry, no cameras are available in your area"}

    return jsonify(response)


if __name__ == "__main__":
    # Debug mode enabled for hackathon/development - disable in production
    app.run(debug=True, host="0.0.0.0", port=5000)  # noqa: S104, S201
