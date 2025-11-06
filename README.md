# Lórien's Guide

Project Hafnia Hackathon: Lórien's Guide - A tool to help the vision impaired in public spaces.

## Overview

Lórien's Guide is an accessibility assistant that uses Vision Language Models (VLM) to help visually impaired users navigate public spaces. The system analyzes video feeds from strategically placed cameras and provides clear, spoken directions based on the user's location and questions.

## How It Works

### Core Logic Flow

1. **Get User Request**: Receives the user's location (`lat`, `long`) and their question (`question_text`) from the mobile app
2. **Find Nearest Camera**: Queries `cameras.json` to find the camera closest to the user's location
3. **Get Video & Context**: Retrieves the video clip URL and context description for the nearest camera
4. **Call Hafnia VLM**: Sends the video clip and a carefully crafted prompt to the VLM API
5. **Get VLM Response**: Receives a JSON object with the text description from the VLM
6. **Relay to User**: Sends the response back to the mobile app, which reads it aloud

### VLM API Prompt

The prompt sent to the VLM is critical to the system's effectiveness:

```
You are an accessibility assistant for a user with vision impairment. 
The user is at the '{location_context}'.

They have asked: '{user_question}'

Analyze the attached video clip of this location. Provide a safe, clear, 
and direct answer. Use landmarks and steps (e.g., 'on your left,' 
'walk 10 steps'), not colors.
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/osquera/Loriens-Guide.git
cd Loriens-Guide
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your VLM API key
```

4. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST `/api/v1/query`

Process a user query and get directions.

**Request Body:**
```json
{
  "lat": 55.6761,
  "long": 12.5683,
  "question_text": "I'm looking for the exit, where is it?"
}
```

**Response:**
```json
{
  "camera_id": "lib_lobby_01",
  "camera_name": "Library Lobby - Main Entrance",
  "question": "I'm looking for the exit, where is it?",
  "answer": "The exit is 20 steps forward. Walk straight ahead, keeping the information desk on your right. You will reach the main doors in approximately 20 steps.",
  "error": false
}
```

### GET `/api/v1/cameras`

List all available cameras.

**Response:**
```json
{
  "cameras": [
    {
      "camera_id": "lib_lobby_01",
      "name": "Library Lobby - Main Entrance",
      "location": {
        "lat": 55.6761,
        "long": 12.5683
      },
      "orientation": "facing east",
      "video_clip_url": "videos/library_lobby.mp4",
      "context_description": "Library Lobby - Main Entrance, facing east"
    }
  ]
}
```

### POST `/api/v1/cameras/nearest`

Find the nearest camera to given coordinates.

**Request Body:**
```json
{
  "lat": 55.6761,
  "long": 12.5683
}
```

**Response:**
```json
{
  "camera": {
    "camera_id": "lib_lobby_01",
    "name": "Library Lobby - Main Entrance",
    "location": {
      "lat": 55.6761,
      "long": 12.5683
    },
    "orientation": "facing east",
    "video_clip_url": "videos/library_lobby.mp4",
    "context_description": "Library Lobby - Main Entrance, facing east"
  }
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Hafnia VLM API"
}
```

## Camera Configuration

Cameras are configured in `cameras.json`. Each camera entry includes:

- `camera_id`: Unique identifier
- `name`: Human-readable name
- `location`: GPS coordinates (lat, long)
- `orientation`: Direction the camera is facing
- `video_clip_url`: Path to video clip
- `context_description`: Detailed description used in VLM prompts

Example:
```json
{
  "camera_id": "lib_lobby_01",
  "name": "Library Lobby - Main Entrance",
  "location": {
    "lat": 55.6761,
    "long": 12.5683
  },
  "orientation": "facing east",
  "video_clip_url": "videos/library_lobby.mp4",
  "context_description": "Library Lobby - Main Entrance, facing east"
}
```

## Architecture

### Components

1. **app.py**: Flask backend server that handles HTTP requests
2. **vlm_service.py**: Core VLM service logic
   - Camera distance calculation
   - Nearest camera finding
   - VLM prompt construction
   - VLM API integration
3. **cameras.json**: Camera configuration database

### Key Features

- **Haversine Distance Calculation**: Accurately finds the nearest camera using GPS coordinates
- **Accessibility-Focused Prompts**: Crafted specifically for vision-impaired users
- **Error Handling**: Graceful degradation when VLM API is unavailable
- **RESTful API**: Clean, documented endpoints for mobile app integration

## Example Usage

### Using curl

```bash
# Find nearest camera
curl -X POST http://localhost:5000/api/v1/cameras/nearest \
  -H "Content-Type: application/json" \
  -d '{"lat": 55.6761, "long": 12.5683}'

# Ask a question
curl -X POST http://localhost:5000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 55.6761,
    "long": 12.5683,
    "question_text": "Where is the bathroom?"
  }'
```

### Using Python

```python
import requests

url = "http://localhost:5000/api/v1/query"
data = {
    "lat": 55.6761,
    "long": 12.5683,
    "question_text": "I'm looking for the exit, where is it?"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Answer: {result['answer']}")
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

The project follows PEP 8 Python style guidelines.

## Environment Variables

- `VLM_API_URL`: URL for the Hafnia VLM API (default: https://api.hafnia.ai/v1/vlm)
- `VLM_API_KEY`: API key for VLM service authentication
- `PORT`: Server port (default: 5000)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Created for the Project Hafnia Hackathon to improve accessibility in public spaces.
