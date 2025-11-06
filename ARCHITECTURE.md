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
# Hafnia VLM API - Architecture and Flow

## System Architecture

```
┌─────────────┐
│ Mobile App  │
│ (User with  │
│  vision     │
│ impairment) │
└──────┬──────┘
       │
       │ HTTP POST /api/v1/query
       │ {lat, long, question_text}
       │
       ▼
┌─────────────────────────────────┐
│   Flask Backend Server          │
│   (app.py)                      │
│                                 │
│   Endpoints:                    │
│   • POST /api/v1/query          │
│   • GET  /api/v1/cameras        │
│   • POST /api/v1/cameras/nearest│
│   • GET  /health                │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│   VLM Service                   │
│   (vlm_service.py)              │
│                                 │
│   Core Functions:               │
│   1. Find Nearest Camera        │
│   2. Construct VLM Prompt       │
│   3. Call VLM API               │
│   4. Process Response           │
└──────┬────────────┬─────────────┘
       │            │
       │            └──────────┐
       │                       │
       ▼                       ▼
┌──────────────┐      ┌─────────────────┐
│ cameras.json │      │  Hafnia VLM API │
│              │      │  (External)     │
│ • Locations  │      │                 │
│ • Videos     │      │ Analyzes video  │
│ • Context    │      │ Returns text    │
└──────────────┘      └─────────────────┘
```

## Request Flow

### 1. User Makes Request

**Mobile App → Backend Server**
```json
POST /api/v1/query
{
  "lat": 55.6761,
  "long": 12.5683,
  "question_text": "I'm looking for the exit, where is it?"
}
```

### 2. Find Nearest Camera

**Backend → VLM Service**

The service:
- Loads camera data from `cameras.json`
- Calculates distance from user to each camera using Haversine formula
- Identifies closest camera

**Result:**
```json
{
  "camera_id": "lib_lobby_01",
  "name": "Library Lobby - Main Entrance",
  "location": {"lat": 55.6761, "long": 12.5683},
  "orientation": "facing east",
  "video_clip_url": "videos/library_lobby.mp4",
  "context_description": "Library Lobby - Main Entrance, facing east"
}
```

### 3. Construct VLM Prompt

**VLM Service → Prompt Builder**

Combines:
- User's question
- Camera context description
- Accessibility-specific instructions

**Generated Prompt:**
```
You are an accessibility assistant for a user with vision impairment. 
The user is at the 'Library Lobby - Main Entrance, facing east'.

They have asked: 'I'm looking for the exit, where is it?'

Analyze the attached video clip of this location. Provide a safe, clear, 
and direct answer. Use landmarks and steps (e.g., 'on your left,' 
'walk 10 steps'), not colors.
```

### 4. Call Hafnia VLM API

**VLM Service → Hafnia VLM**
```json
POST https://api.hafnia.ai/v1/vlm
Headers: {
  "Authorization": "Bearer {API_KEY}",
  "Content-Type": "application/json"
}
Body: {
  "video_url": "videos/library_lobby.mp4",
  "prompt": "You are an accessibility assistant...",
  "max_tokens": 500
}
```

### 5. Receive VLM Response

**Hafnia VLM → VLM Service**
```json
{
  "text": "The exit is 20 steps forward. Walk straight ahead, keeping the 
           information desk on your right. You will reach the main doors 
           in approximately 20 steps. The doors open automatically."
}
```

### 6. Return to Mobile App

**Backend → Mobile App**
```json
{
  "camera_id": "lib_lobby_01",
  "camera_name": "Library Lobby - Main Entrance",
  "question": "I'm looking for the exit, where is it?",
  "answer": "The exit is 20 steps forward. Walk straight ahead, keeping 
             the information desk on your right. You will reach the main 
             doors in approximately 20 steps. The doors open automatically.",
  "error": false
}
```

### 7. Text-to-Speech

**Mobile App**
- Receives the answer text
- Uses text-to-speech to read it aloud to the user
- User now knows exactly how to reach the exit

## Key Components

### Haversine Distance Formula

Used to calculate the distance between two GPS coordinates on a sphere:

```python
def _calculate_distance(lat1, long1, lat2, long2):
    R = 6371000  # Earth's radius in meters
    
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
    
    return R * c  # Distance in meters
```

### VLM Prompt Design

The prompt is carefully designed for accessibility:

**Key Elements:**
1. **Role Definition**: "accessibility assistant for a user with vision impairment"
2. **Context**: Precise location and orientation
3. **User Question**: Exact user query
4. **Task**: "Analyze the attached video clip"
5. **Instructions**:
   - Safe, clear, and direct
   - Use landmarks and steps
   - Avoid color-based directions
   - Use directional cues (left, right, forward)

**Why This Matters:**
- Vision-impaired users can't use visual cues like colors
- Step counts provide concrete distance measurements
- Landmarks (e.g., "information desk") provide confirmation points
- Safety is paramount in navigation assistance

## Error Handling

### Network Errors
```json
{
  "error": true,
  "message": "Failed to connect to VLM API",
  "text": "I'm sorry, I'm having trouble connecting to the vision service. 
          Please try again."
}
```

### No Cameras Available
```json
{
  "error": true,
  "message": "No cameras available in your area",
  "text": "I'm sorry, there are no cameras available in your area."
}
```

### Invalid Input
```json
{
  "error": true,
  "message": "Missing required fields: question_text"
}
```

## Security Features

1. **No Debug Mode in Production**: Debug disabled by default
2. **Sanitized Error Messages**: No stack traces exposed
3. **Input Validation**: All inputs validated before processing
4. **API Key Security**: Keys stored in environment variables
5. **CORS Configuration**: Configured for mobile app access

## Performance Considerations

1. **Nearest Camera**: O(n) complexity, fast for reasonable camera counts
2. **API Timeout**: 30-second timeout on VLM API calls
3. **Error Recovery**: Graceful degradation on API failures
4. **Caching Potential**: Could cache common question responses

## Extensibility

### Adding New Cameras
1. Add entry to `cameras.json`
2. Place video file in `videos/` directory
3. No code changes needed

### Supporting Multiple Languages
1. Modify prompt construction to include language parameter
2. Add language field to request payload
3. VLM will respond in requested language

### Adding Context
- Current weather
- Time of day
- Event information
- Building status (open/closed)

Can be added to the prompt dynamically.

## Testing

### Unit Tests (test_vlm_service.py)
- Distance calculation
- Nearest camera finding
- Prompt construction
- API integration (mocked)
- Complete request processing

### Integration Tests (test_app.py)
- Health check endpoint
- Camera listing
- Nearest camera endpoint
- Query endpoint with validation
- Error handling

**All tests passing: 16/16 ✓**

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions for:
- Local development
- Docker
- AWS Elastic Beanstalk
- Google Cloud Run
- Heroku

## Future Enhancements

1. **Database Integration**: Move from JSON to database
2. **Real-time Video**: Stream live video instead of clips
3. **Multi-camera Support**: Analyze multiple camera views
4. **Indoor Positioning**: More accurate positioning using beacons
5. **Crowdsourced Updates**: Community-contributed camera additions
6. **Voice Input**: Direct voice-to-voice interaction
7. **Haptic Feedback**: Vibration patterns for navigation cues
