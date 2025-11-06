"""Hafnia VLM API Backend Server.

This backend server receives requests from the mobile app and processes them
using the VLM service to provide accessibility assistance.
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS

from vlm_service import VLMService

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize VLM service
vlm_service = VLMService()


@app.route("/health", methods=["GET"])
def health_check()-> tuple[Response, int]:
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Hafnia VLM API"}), 200


@app.route("/api/v1/query", methods=["POST"])
def process_query() -> tuple[Response, int]:
    """Main endpoint for processing user queries.

    Expected JSON payload:
    {
        "lat": 55.6761,
        "long": 12.5683,
        "question_text": "I'm looking for the exit, where is it?"
    }

    Returns JSON response:
    {
        "camera_id": "lib_lobby_01",
        "camera_name": "Library Lobby - Main Entrance",
        "question": "I'm looking for the exit, where is it?",
        "answer": "The exit is 20 steps forward...",
        "error": false
    }
    """  # noqa: D401
    # Validate request
    if not request.is_json:
        return jsonify({"error": True, "message": "Request must be JSON"}), 400

    data = request.get_json()

    # Validate required fields
    required_fields = ["lat", "long", "question_text"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": True, "message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Extract parameters
    try:
        lat = float(data["lat"])
        long = float(data["long"])
        question_text = str(data["question_text"])
    except (ValueError, TypeError):
        return jsonify({"error": True, "message": "Invalid parameter types"}), 400

    # Process the request
    response = vlm_service.process_user_request(lat, long, question_text)

    # Return response
    status_code = 500 if response.get("error", False) else 200
    return jsonify(response), status_code


@app.route("/api/v1/cameras", methods=["GET"])
def list_cameras() -> tuple[Response, int]:
    """List all available cameras.

    Returns JSON response with all cameras and their locations.
    """
    return jsonify({"cameras": vlm_service.cameras}), 200


@app.route("/api/v1/cameras/nearest", methods=["POST"])
def find_nearest_camera() -> tuple[Response, int]:
    """Find the nearest camera to given coordinates.

    Expected JSON payload:
    {
        "lat": 55.6761,
        "long": 12.5683
    }

    Returns the nearest camera information.
    """
    if not request.is_json:
        return jsonify({"error": True, "message": "Request must be JSON"}), 400

    data = request.get_json()

    # Validate required fields
    if "lat" not in data or "long" not in data:
        return jsonify({"error": True, "message": "Missing required fields: lat, long"}), 400

    try:
        lat = float(data["lat"])
        long = float(data["long"])
    except (ValueError, TypeError):
        return jsonify({"error": True, "message": "Invalid parameter types"}), 400

    # Find nearest camera
    nearest_camera = vlm_service.find_nearest_camera(lat, long)

    if nearest_camera:
        return jsonify({"camera": nearest_camera}), 200
    return jsonify({"error": True, "message": "No cameras available"}), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # noqa: PLW1508
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)  # noqa: S104
