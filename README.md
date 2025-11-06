# Lórien's Guide
Project Hafnia Hackathon: Lórien's Guide: A tool to help the vision impaired in public spaces.

## Overview

Lórien's Guide is an assistive technology solution designed to help vision-impaired individuals navigate public spaces using location-based video context and AI assistance.

## Project Structure

```
Loriens-Guide/
├── database/           # Camera registry database
│   ├── cameras.json   # Maps video clips to GPS coordinates
│   └── README.md      # Database documentation
├── videos/            # Pre-recorded video clips
│   └── README.md      # Video requirements and guidelines
└── README.md          # This file
```

## Camera Registry Database

The camera registry is the core component of this PoC. It maps pre-recorded video clips to specific GPS coordinates, allowing the system to provide location-based visual context without requiring access to real camera feeds.

### Key Features

- **JSON-based database** (`database/cameras.json`)
- **4 demo locations** including library, park, train station, and coffee shop
- **GPS coordinate mapping** for location-based queries
- **Contextual descriptions** for each location

### Sample Camera Entry

```json
{
  "camera_id": "lib_lobby_01",
  "name": "Library Lobby - Main Entrance",
  "location": {
    "lat": 40.7128,
    "long": -74.0060
  },
  "video_clip_url": "videos/library_lobby.mp4",
  "context_description": "User is at the library main entrance, facing east."
}
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/osquera/Loriens-Guide.git
   cd Loriens-Guide
   ```

2. **Add video clips**
   - Place your pre-recorded video clips in the `videos/` directory
   - See `videos/README.md` for video requirements

3. **Explore the camera registry**
   - Check `database/cameras.json` for available locations
   - See `database/README.md` for detailed documentation

## Future Development

This PoC demonstrates the core concept. Future enhancements could include:

- Migration to MongoDB Atlas (free tier) for scalable database
- Integration with real camera feeds (with proper permissions)
- Mobile application for vision-impaired users
- AI-powered scene description and navigation assistance
- Real-time location tracking and guidance

## Contributing

This is a hackathon project. Contributions and improvements are welcome!

## License

TBD
