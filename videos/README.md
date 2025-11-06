# Video Files Directory

This directory should contain video clips for each camera location referenced in `cameras.json`.

## Required Video Files

Based on the current camera configuration, the following video files should be placed in this directory:

1. `library_lobby.mp4` - Library Lobby Main Entrance view
2. `library_floor2.mp4` - Library Second Floor Study Area view
3. `library_exit.mp4` - Library Exit West Door view

## Video Requirements

- **Format**: MP4 (H.264 codec recommended)
- **Duration**: 5-10 seconds for optimal VLM processing
- **Resolution**: 720p or higher
- **Frame Rate**: 24-30 fps
- **Content**: Should clearly show the area from the camera's perspective
- **Orientation**: Must match the orientation specified in cameras.json

## Adding New Videos

When adding a new camera to `cameras.json`:

1. Place the video file in this directory
2. Update the `video_clip_url` field in cameras.json to reference the file
3. Ensure the video captures the perspective described in `context_description`

## Note

Video files are not included in the repository due to size. They should be:
- Stored in a separate media storage system
- Uploaded to this directory during deployment
- Or referenced via external URLs in the cameras.json configuration
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
