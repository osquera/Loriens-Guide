# Loriens-Guide
Project Hafnia Hackathon: Lórien's Guide: A tool to help the vision impaired in public spaces.

## Backend Server

The backend is built with FastAPI and provides a REST API for guidance queries.

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python server.py
```

The server will start on `http://localhost:8000`

### API Endpoint

#### POST /api/get-guidance

Provides guidance based on location and user question.

**Request Body:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "question_text": "I'm looking for the exit, where is it?"
}
```

**Response:**
```json
{
  "answer_text": "You are facing the main hall. The exit is 20 steps forward, just past the large red sculpture on your left."
}
```

### API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`
