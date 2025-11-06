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
