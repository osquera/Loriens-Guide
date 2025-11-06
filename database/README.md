# Camera Registry Database

This directory contains the camera registry database for Lórien's Guide PoC (Proof of Concept).

## Overview

The camera registry maps pre-recorded video clips to specific GPS coordinates. This is a key component of the demo that allows the system to provide location-based visual assistance without requiring access to real camera feeds.

## Structure

### cameras.json

The main database file that contains camera location data with the following schema:

```json
{
  "camera_id": "unique_identifier",
  "name": "Human-readable camera name",
  "location": {
    "lat": 40.7128,
    "long": -74.0060
  },
  "video_clip_url": "path/to/video.mp4",
  "context_description": "Description of what the user sees at this location"
}
```

### Fields

- **camera_id**: Unique identifier for the camera location
- **name**: Human-readable name describing the location
- **location**: GPS coordinates
  - **lat**: Latitude (decimal degrees)
  - **long**: Longitude (decimal degrees)
- **video_clip_url**: Relative path to the pre-recorded video clip
- **context_description**: Contextual information about what a user would experience at this location

## Demo Locations

The current database includes 4 sample locations:

1. **Library Lobby** - Main entrance (lib_lobby_01)
2. **City Park** - Fountain area (park_fountain_01)
3. **Central Train Station** - Platform 3 (train_station_01)
4. **Main Street Coffee Shop** - Entrance (coffee_shop_01)

## Usage

Applications can load this JSON file to:
- Query camera locations based on user GPS coordinates
- Retrieve the appropriate video clip for a given location
- Provide context-aware assistance to vision-impaired users

## Future Enhancements

For production deployment, consider:
- Migrating to a proper database (e.g., MongoDB Atlas free tier)
- Adding authentication and access control
- Implementing real-time camera feed integration
- Expanding location coverage
