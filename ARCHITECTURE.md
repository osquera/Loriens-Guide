# Lórien's Guide - Architecture Documentation

## System Overview

Lórien's Guide is a hackathon project designed to assist vision-impaired individuals in navigating public spaces using Vision Language Models (VLM) and voice interaction.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                             │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               Mobile Web Interface (Frontend)                │   │
│  │                                                               │   │
│  │  • Voice Input (Web Speech API - STT)                        │   │
│  │  • Voice Output (Web Speech API - TTS)                       │   │
│  │  • High Contrast UI (Accessibility)                          │   │
│  │  • Geolocation Services                                      │   │
│  │  • Quick Action Buttons                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                 │                                     │
│                                 │ HTTPS/REST API                      │
│                                 ▼                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     BACKEND ORCHESTRATOR                             │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 Flask REST API Server                        │   │
│  │                                                               │   │
│  │  Core Services:                                              │   │
│  │  ├─ Camera Registry Manager                                  │   │
│  │  ├─ Location Service (Nearby Camera Lookup)                  │   │
│  │  ├─ VLM Integration Service                                  │   │
│  │  ├─ Voice Processing Coordinator                             │   │
│  │  └─ Assistance Request Orchestrator                          │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                  │              │              │                      │
│                  │              │              │                      │
│                  ▼              ▼              ▼                      │
│         ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│         │   Camera    │ │   Hafnia    │ │   Voice     │            │
│         │  Registry   │ │     VLM     │ │  Services   │            │
│         │   (JSON)    │ │  (External) │ │  (STT/TTS)  │            │
│         └─────────────┘ └─────────────┘ └─────────────┘            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       EXTERNAL SERVICES                              │
│                                                                       │
│  ┌─────────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │   Hafnia VLM API    │  │  STT/TTS APIs    │  │  Public Camera │ │
│  │                     │  │  (Optional)      │  │     Feeds      │ │
│  │  • Scene Analysis   │  │  • Transcription │  │  • Live Video  │ │
│  │  • Object Detection │  │  • Synthesis     │  │  • Snapshots   │ │
│  │  • Text Recognition │  │  • Multi-lang    │  │                │ │
│  └─────────────────────┘  └──────────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (Mobile Web App)

**Purpose**: Provide accessible, voice-first interface for users

**Technology Stack**:
- HTML5 for semantic structure
- CSS3 for high-contrast styling
- Vanilla JavaScript (ES6+)
- Web Speech API (native browser support)
- Geolocation API (native browser support)

**Key Features**:
- Large touch targets (200x200px voice button)
- High contrast color scheme (black/white/green)
- Voice-first interaction model
- Text input fallback
- Screen reader compatible
- WCAG AAA accessibility compliance

**Files**:
- `/frontend/index.html` - Main page structure
- `/frontend/styles.css` - Accessible styling
- `/frontend/app.js` - Application logic

### 2. Backend Orchestrator

**Purpose**: Coordinate services and handle business logic

**Technology Stack**:
- Python 3.8+
- Flask (lightweight web framework)
- Flask-CORS (cross-origin support)
- JSON file-based storage

**Key Responsibilities**:
1. **Camera Management**:
   - Load and maintain camera registry
   - Find cameras by location
   - Provide camera metadata
   
2. **Location Services**:
   - Accept user location
   - Calculate nearby cameras
   - Return relevant camera information
   
3. **VLM Integration**:
   - Interface with Hafnia VLM API
   - Format queries for VLM
   - Process VLM responses
   
4. **Voice Processing**:
   - Coordinate STT/TTS operations
   - Handle voice query transcription
   - Generate voice responses
   
5. **Request Orchestration**:
   - Main assistance endpoint
   - Combine multiple services
   - Return unified responses

**API Endpoints**:
```
GET  /api/health                  - Health check
GET  /api/cameras                 - List all cameras
GET  /api/cameras/<id>            - Get specific camera
POST /api/cameras/nearby          - Find nearby cameras
POST /api/vlm/analyze             - VLM scene analysis
POST /api/voice/transcribe        - Speech-to-text
POST /api/voice/synthesize        - Text-to-speech
POST /api/assistance/request      - Main assistance flow
```

**Files**:
- `/backend/app.py` - Main Flask application
- `/backend/requirements.txt` - Python dependencies
- `/backend/camera_registry.json` - Camera database

### 3. Camera Registry

**Purpose**: Simple database of available public cameras

**Data Model**:
```json
{
  "cameras": [
    {
      "id": "string",           // Unique identifier
      "name": "string",         // Human-readable name
      "location": {
        "latitude": float,
        "longitude": float,
        "address": "string"     // Human-readable address
      },
      "description": "string",  // Scene description
      "status": "string",       // active/inactive/maintenance
      "coverage_area": "string",// Area description
      "capabilities": [         // Supported features
        "object_detection",
        "text_recognition",
        "person_detection"
      ]
    }
  ]
}
```

**Operations**:
- Read all cameras
- Find camera by ID
- Filter by location (nearby)
- Check camera status

### 4. External APIs

#### Hafnia VLM (Vision Language Model)
**Status**: Placeholder integration

**Purpose**:
- Analyze camera feeds
- Describe scenes
- Detect objects and people
- Read text and signs
- Answer visual questions

**Integration Points**:
- Endpoint: `/api/vlm/analyze`
- Expected input: Camera ID, query text
- Expected output: Analysis, confidence score

**Future Implementation**:
```python
# Example integration code
import hafnia_vlm_sdk

def analyze_with_vlm(camera_id, query):
    camera_feed = get_camera_feed(camera_id)
    result = hafnia_vlm_sdk.analyze(
        image=camera_feed,
        query=query,
        features=['scene_description', 'object_detection', 'ocr']
    )
    return result
```

#### STT/TTS Services
**Current**: Web Speech API (browser-native)
**Future**: Cloud-based services for enhanced quality

**Potential Services**:
- Google Cloud Speech-to-Text / Text-to-Speech
- Azure Speech Services
- Amazon Transcribe / Polly
- Open source alternatives (Mozilla DeepSpeech, Coqui TTS)

## Data Flow

### Main Assistance Flow

1. **User Request**:
   ```
   User speaks → Web Speech API → Frontend JavaScript
   ```

2. **Request Processing**:
   ```
   Frontend → POST /api/assistance/request → Backend
   {
     "location": {"latitude": 55.6761, "longitude": 12.5683},
     "query": "What do you see?"
   }
   ```

3. **Backend Processing**:
   ```
   Backend receives request
     ↓
   Load camera registry
     ↓
   Find nearest camera(s) based on location
     ↓
   If camera found:
     ├─ Get camera feed
     ├─ Call Hafnia VLM API
     ├─ Process VLM response
     └─ Generate voice-friendly response
   Else:
     └─ Generate "no cameras available" response
   ```

4. **Response Delivery**:
   ```
   Backend → Response JSON → Frontend
   {
     "camera": {...},
     "analysis": "Scene description",
     "voice_response": "I can see...",
     "timestamp": "2025-11-06T21:04:29Z"
   }
   ```

5. **Voice Output**:
   ```
   Frontend → Web Speech API → Speaker
   Display text response on screen
   ```

## Security Considerations

1. **Privacy**:
   - No user data storage
   - Camera feeds processed in real-time only
   - Location used transiently for camera lookup
   - No session tracking

2. **CORS**:
   - Enabled for development
   - Should be restricted to specific origins in production

3. **API Keys**:
   - Use environment variables
   - Never commit secrets to repository
   - Implement rate limiting

4. **Camera Access**:
   - Ensure proper authorization for camera feed access
   - Comply with public camera usage regulations
   - Respect privacy laws

## Deployment Considerations

### Development
- Backend: `python app.py` (Flask development server)
- Frontend: Direct file access or simple HTTP server

### Production (Future)
- Backend: Gunicorn/uWSGI with Flask
- Frontend: Static file hosting (CDN, S3, etc.)
- Database: Migrate from JSON to PostgreSQL/MongoDB
- Caching: Redis for camera registry and responses
- Load Balancing: Nginx reverse proxy
- Monitoring: Application performance monitoring
- Logging: Centralized logging system

## Scalability Path

1. **Phase 1 (Current)**: Single server, file-based storage
2. **Phase 2**: Database migration, API caching
3. **Phase 3**: Multiple backend instances, load balancing
4. **Phase 4**: Microservices architecture
   - Camera service
   - VLM service
   - Voice service
   - Orchestration service

## Testing Strategy

### Frontend
- Manual testing with screen readers
- Accessibility audits (WAVE, axe)
- Voice interaction testing
- Cross-browser compatibility

### Backend
- Unit tests for each endpoint
- Integration tests for service orchestration
- Load testing for API performance
- Mock VLM API responses

### End-to-End
- Complete user flow testing
- Voice input to voice output
- Error handling scenarios
- Network failure resilience

## Future Enhancements

1. **Enhanced VLM Integration**:
   - Real-time video analysis
   - Object tracking
   - Predictive scene understanding

2. **Advanced Navigation**:
   - Turn-by-turn directions
   - Obstacle detection
   - Safe route calculation

3. **Multi-Language Support**:
   - Multiple STT/TTS languages
   - Localized responses
   - Cultural adaptations

4. **Offline Capabilities**:
   - Cached responses
   - Local processing
   - Progressive Web App

5. **User Personalization**:
   - Preferences storage
   - Custom quick actions
   - Favorite locations

6. **Community Features**:
   - User-reported issues
   - Camera quality ratings
   - Crowdsourced improvements

---

**Document Version**: 1.0
**Last Updated**: 2025-11-06
**Maintained By**: Project Hafnia Hackathon Team
