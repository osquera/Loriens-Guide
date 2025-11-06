# Lórien's Guide

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
