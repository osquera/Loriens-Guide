# Lórien's Guide

**Project Hafnia Hackathon**: A tool to help the vision impaired in public spaces.

## Architecture Overview

Lórien's Guide is a voice-first accessibility tool that leverages Vision Language Models (VLM) to help vision-impaired individuals navigate public spaces. The system integrates with public cameras to provide real-time scene descriptions and navigation assistance.

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      LÓRIEN'S GUIDE                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│   Frontend   │◄──────►│   Backend    │◄──────►│   Camera     │
│  (Web App)   │        │ Orchestrator │        │   Registry   │
└──────────────┘        └──────────────┘        └──────────────┘
      │                        │
      │                        │
      ▼                        ▼
┌──────────────┐        ┌──────────────┐
│   Voice I/O  │        │  Hafnia VLM  │
│  (STT/TTS)   │        │     API      │
└──────────────┘        └──────────────┘
```

#### 1. Frontend (Mobile Web App)
- **Purpose**: Voice-first, high-contrast interface for vision-impaired users
- **Features**:
  - Large, accessible buttons and controls
  - Voice input/output via Web Speech API
  - High contrast color scheme (black background, green accents)
  - Screen reader compatible
  - Quick action buttons for common queries
  - Real-time camera status display
- **Technology**: Pure HTML/CSS/JavaScript (no build required)
- **Location**: `/frontend/`

#### 2. Backend (The Orchestrator)
- **Purpose**: Lightweight server handling business logic and API orchestration
- **Features**:
  - Camera registry management
  - Location-based camera lookup
  - VLM API integration (Hafnia)
  - Voice processing coordination (STT/TTS)
  - Request/response orchestration
- **Technology**: Python Flask
- **Location**: `/backend/`
- **API Endpoints**:
  - `GET /api/health` - Health check
  - `GET /api/cameras` - Get all cameras
  - `GET /api/cameras/<id>` - Get specific camera
  - `POST /api/cameras/nearby` - Find nearby cameras
  - `POST /api/vlm/analyze` - Analyze scene with VLM
  - `POST /api/voice/transcribe` - Speech-to-text
  - `POST /api/voice/synthesize` - Text-to-speech
  - `POST /api/assistance/request` - Main assistance endpoint

#### 3. Camera Registry
- **Purpose**: Simple database of available public cameras
- **Format**: JSON file with camera locations and metadata
- **Location**: `/backend/camera_registry.json`
- **Data Structure**:
  ```json
  {
    "cameras": [
      {
        "id": "cam001",
        "name": "Location Name",
        "location": {"latitude": 55.6761, "longitude": 12.5683},
        "description": "Scene description",
        "status": "active",
        "capabilities": ["object_detection", "text_recognition"]
      }
    ]
  }
  ```

#### 4. External APIs (Integration Points)

##### Hafnia VLM (Vision Language Model)
- **Purpose**: The star of the show - analyzes camera feeds
- **Integration**: `/api/vlm/analyze` endpoint
- **Usage**: Scene understanding, object detection, text reading
- **Status**: Placeholder implementation (integrate with actual Hafnia VLM API)

##### STT/TTS Services
- **Purpose**: Voice input/output for accessibility
- **Integration**: 
  - Frontend: Web Speech API (built into browsers)
  - Backend: `/api/voice/*` endpoints for server-side processing
- **Status**: Frontend uses native browser API; backend has placeholder for enhanced services

## Getting Started

### Prerequisites
- Python 3.8+
- Modern web browser with Web Speech API support (Chrome, Edge, Safari)

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

**Note**: The server runs in debug mode for development/hackathon purposes. For production deployment, disable debug mode by setting `debug=False` in `app.py`.

### Frontend Setup

1. Open `frontend/index.html` in a web browser, or
2. Serve with a simple HTTP server:
```bash
cd frontend
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

### Configuration

#### Backend Configuration
- Edit `backend/camera_registry.json` to add/modify cameras
- Configure VLM API endpoint in `backend/app.py`
- Set environment variables for API keys (when integrating real services)

#### Frontend Configuration
- Edit `frontend/app.js` CONFIG object:
  ```javascript
  const CONFIG = {
      backendUrl: 'http://localhost:5000',
      speechRecognitionLanguage: 'en-US',
      autoRefreshInterval: 30000
  };
  ```

## Usage

### For Users
1. Open the web app on your mobile device
2. Tap the large green "Tap to Speak" button
3. Ask questions like:
   - "What do you see?"
   - "Can you read any signs?"
   - "Help me navigate"
4. Use quick action buttons for common requests
5. The app will speak responses back to you

### For Developers

#### Adding New Cameras
Edit `backend/camera_registry.json`:
```json
{
  "id": "cam006",
  "name": "New Location",
  "location": {"latitude": 55.0, "longitude": 12.0},
  "description": "Description of the area",
  "status": "active",
  "capabilities": ["object_detection", "text_recognition"]
}
```

#### Integrating Hafnia VLM
Replace the placeholder in `backend/app.py`:
```python
@app.route('/api/vlm/analyze', methods=['POST'])
def analyze_with_vlm():
    # Replace with actual Hafnia VLM API call
    # Example:
    # response = hafnia_vlm.analyze(camera_feed, query)
    pass
```

#### Adding STT/TTS Services
Integrate services like Google Cloud Speech-to-Text or Azure Speech Services in the backend endpoints.

## API Documentation

### Main Assistance Endpoint
```
POST /api/assistance/request
Content-Type: application/json

{
  "location": {
    "latitude": 55.6761,
    "longitude": 12.5683
  },
  "query": "What do you see?"
}

Response:
{
  "camera": {...},
  "analysis": "Scene description from VLM",
  "voice_response": "Spoken response text",
  "timestamp": "2025-11-06T21:04:29.521Z"
}
```

### VLM Analysis
```
POST /api/vlm/analyze
Content-Type: application/json

{
  "camera_id": "cam001",
  "query": "Describe the scene"
}

Response:
{
  "camera_id": "cam001",
  "analysis": "VLM analysis result",
  "confidence": 0.85
}
```

## Design Principles

### Simplicity First
- Minimal dependencies
- No complex build process
- Easy to understand and modify
- Hackathon-ready

### Accessibility
- Voice-first interface
- High contrast colors (WCAG AAA compliant)
- Large touch targets (min 44x44px)
- Screen reader compatible
- Keyboard navigation support

### Privacy & Security
- No user data stored
- Camera feeds processed in real-time only
- Location used only for camera lookup
- CORS enabled for local development

## Future Enhancements

- [ ] Real Hafnia VLM API integration
- [ ] Enhanced STT/TTS with multiple language support
- [ ] Offline mode with cached responses
- [ ] User preferences and customization
- [ ] Navigation directions with haptic feedback
- [ ] Emergency assistance button
- [ ] Multi-camera view synthesis
- [ ] Object tracking and alerts

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Web Speech API
- **Backend**: Python 3, Flask, Flask-CORS
- **Data Storage**: JSON (file-based for simplicity)
- **APIs**: 
  - Hafnia VLM (to be integrated)
  - Web Speech API (browser native)
  - Geolocation API (browser native)

## Contributing

This is a hackathon project focused on rapid prototyping. Contributions should maintain the simplicity and accessibility focus.

## License

MIT License - Free to use and modify for accessibility purposes.

## Acknowledgments

- Project Hafnia Hackathon
- Vision-impaired community for inspiration
- Public transportation authorities for camera access concept

---

**Built with ❤️ for accessibility**
Project Hafnia Hackathon: A voice-enabled mobile web application to help the vision impaired navigate public spaces.

## Features

- 🌍 **GPS Location Tracking**: Real-time location access using `navigator.geolocation` API
- 🎤 **Speech-to-Text**: Voice input using Web Speech API (`SpeechRecognition`)
- 🔊 **Text-to-Speech**: Audio responses using Web Speech API (`speechSynthesis`)
- 📱 **Mobile-First Design**: Responsive web interface optimized for mobile devices
- ♿ **Accessibility**: Large, easy-to-use "Tap to Talk" button interface

## Live Demo Access

Simply open `index.html` in a modern web browser (Chrome, Edge, or Safari recommended) to try the application.

### Requirements

- Modern web browser with Web Speech API support (Chrome 33+, Edge 79+, Safari 14.1+)
- HTTPS or localhost (required for microphone and location access)
- Microphone access permission
- Location services enabled (optional but recommended)

## How to Use

1. **Grant Permissions**: Allow microphone and location access when prompted
2. **Tap the Button**: Press the large "Tap to Talk" button
3. **Ask Your Question**: Speak naturally - ask about your location, directions, or surroundings
4. **Listen to Response**: The app will read the answer aloud using text-to-speech

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **APIs**: 
  - Geolocation API for GPS tracking
  - Web Speech API for speech recognition and synthesis
- **No Backend Required**: Fully client-side demo application

## Development

This is a single-page application with no build process required. Simply edit the files and refresh your browser:

- `index.html` - Main HTML structure
- `styles.css` - Styling and responsive design
- `app.js` - JavaScript application logic

## Future Enhancements

In a production version, this app would integrate with:
- Vision-Language Models (VLM) for scene understanding
- Computer vision for object detection and scene analysis
- Backend API for processing complex queries
- Offline support with service workers
- Multi-language support

## Browser Compatibility

| Feature | Chrome | Edge | Safari | Firefox |
|---------|--------|------|--------|---------|
| Geolocation | ✅ | ✅ | ✅ | ✅ |
| Speech Recognition | ✅ | ✅ | ✅ | ❌ |
| Speech Synthesis | ✅ | ✅ | ✅ | ✅ |

**Note**: Firefox doesn't support the Web Speech API's SpeechRecognition feature. Use Chrome, Edge, or Safari for the full experience.

## License

This project was created for the Hafnia Hackathon.
