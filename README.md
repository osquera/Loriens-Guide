# Lórien's Guide

**Project Hafnia Hackathon**: AI-powered accessibility tool for vision-impaired navigation

> 🎥 **Powered by Milestone VLM API** (NVIDIA Cosmos-Reason1)  
> 🌐 **Live Demo**: [loriensguide.osquera.com](https://loriensguide.osquera.com/)

## Overview

Lórien's Guide helps vision-impaired individuals navigate public spaces using AI-powered video analysis. Users ask questions via voice, and the system analyzes nearby camera feeds to provide clear, spoken guidance.

**Key Features:**
- 🎤 Voice-first interface (Web Speech API)
- 🗺️ GPS-based camera selection
- ♿ High contrast, screen reader compatible
- 🤖 AI video analysis (NVIDIA Cosmos-Reason1)
- 📱 Mobile-optimized web app

## Architecture

```
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│   Frontend   │◄──────►│   Backend    │◄──────►│  Milestone   │
│  (Cloudflare)│        │   (Flask)    │        │   VLM API    │
└──────────────┘        └──────────────┘        └──────────────┘
```

- **Frontend**: Static HTML/CSS/JS hosted on Cloudflare Pages
- **Backend**: Python Flask orchestrator (Camera registry + VLM integration)
- **VLM API**: Milestone Hackathon API for video analysis

## Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your HACKATHON_API_KEY and HACKATHON_API_SECRET

# 3. Test the VLM integration
python test_hackathon_api.py --video videos/test_video.mp4

# 4. Run the backend
python backend/app.py
# Backend runs on http://localhost:5000

# 5. Open frontend
# Navigate to http://localhost:5000 in your browser
```

### Deploy Backend

See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway deployment instructions

## Usage

Visit [loriensguide.osquera.com](https://loriensguide.osquera.com/) or run locally:

1. Tap the large "Tap to Speak" button
2. Grant microphone and location permissions
3. Ask questions like:
   - "What do you see?"
   - "Can you read any signs?"
   - "Help me navigate"
4. Listen to the spoken response

## For Developers

### Adding Cameras

Edit `backend/camera_registry.json`:
```json
{
  "id": "cam006",
  "name": "New Location",
  "location": {"latitude": 55.0, "longitude": 12.0},
  "status": "active"
}
```

### API Endpoints

- `GET /api/health` - Health check
- `GET /api/cameras` - List all cameras
- `POST /api/cameras/nearby` - Find nearby cameras
- `POST /api/vlm/analyze` - VLM video analysis

See [HACKATHON_API.md](HACKATHON_API.md) for detailed API documentation

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Web Speech API)
- **Backend**: Python 3.12, Flask, Flask-CORS
- **VLM**: Milestone Hackathon API (NVIDIA Cosmos-Reason1)
- **Hosting**: Cloudflare Pages (frontend), Railway (backend)

## Documentation

- **[API Integration Guide](HACKATHON_API.md)** - Milestone VLM API details
- **[Deployment Guide](DEPLOYMENT.md)** - Backend hosting on Railway
- **[Architecture Details](ARCHITECTURE.md)** - System design

## Project Status

| Component | Status |
|-----------|--------|
| Frontend | ✅ Live at loriensguide.osquera.com |
| Backend | 🚧 Ready to deploy |
| VLM Integration | ✅ Production ready |

## Acknowledgments

- **Milestone Systems** & **NVIDIA** - VLM API access
- **Project Hafnia** - Hackathon organizers
- **Vision-impaired community** - Inspiration

---

**Built with ❤️ for accessibility** | MIT License 
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
