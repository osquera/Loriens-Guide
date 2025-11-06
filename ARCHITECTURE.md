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
