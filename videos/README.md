# Video Clips Directory

This directory stores pre-recorded video clips for the camera registry locations.

## Purpose

For the Lórien's Guide PoC, instead of connecting to real camera feeds, we use pre-recorded video clips mapped to specific GPS coordinates. This allows us to demonstrate the system's functionality without the complexity of live camera integration.

## Expected Video Files

Based on the camera registry (`../database/cameras.json`), the following video files should be placed in this directory:

1. `library_lobby.mp4` - Video of the library main entrance
2. `park_fountain.mp4` - Video of the city park fountain area
3. `train_station.mp4` - Video of central train station platform 3
4. `coffee_shop.mp4` - Video of the Main Street coffee shop entrance

## Video Requirements

For best results, video clips should:

- **Duration**: 30-60 seconds of relevant footage
- **Format**: MP4 (H.264 codec recommended for broad compatibility)
- **Resolution**: 720p or 1080p
- **Content**: Show the location from a first-person perspective
- **Quality**: Clear, well-lit footage that captures important details

## Adding New Videos

1. Record or obtain video footage of the location
2. Save the file with a descriptive name (e.g., `location_name.mp4`)
3. Add the video file to this directory
4. Update the camera registry in `../database/cameras.json` with the corresponding entry

## Note

Video files are not included in the repository due to size constraints. For demo purposes, add your own video clips to this directory before running the application.

## Placeholder Videos

If you don't have real footage, you can use:
- Sample videos from free stock footage sites (Pexels, Pixabay)
- Simple screen recordings of location photos
- Test pattern videos for development purposes
