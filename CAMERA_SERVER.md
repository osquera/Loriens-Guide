# Camera Server Setup

This sets up your laptop camera as a "CCTV camera" for the Lórien's Guide system.

## Quick Start

### 1. Install Dependencies

```bash
pip install opencv-python
```

### 2. Run the Camera Server

```bash
python camera_server.py
```

This will:
- ✅ Open your laptop webcam
- 📹 Record continuous 5-second video clips
- 💾 Save them to `/videos/laptop_camera_latest.mp4`
- 🔄 Update the clip every 5 seconds

### 3. Test the System

The camera is now registered as `laptop_camera` in the system. When users ask questions through the mobile app:

1. **User speaks**: "What do you see?"
2. **Frontend**: Sends request with GPS location
3. **Backend**: Finds nearest camera (`laptop_camera`)
4. **Backend**: Uploads latest video clip to Milestone VLM API
5. **VLM**: Analyzes the video
6. **Frontend**: Speaks the AI response to the user

## Options

### Custom camera device
```bash
python camera_server.py --camera 1
```

### Custom clip duration
```bash
python camera_server.py --duration 10
```
(Records 10-second clips instead of 5)

### Headless mode
To run without video preview window, comment out the `cv2.imshow()` line in `camera_server.py`

## How It Works

```
┌─────────────────┐
│ Laptop Camera   │ 📹
└────────┬────────┘
         │ Captures video
         ▼
┌─────────────────┐
│ camera_server.py│ Records 5s clips
└────────┬────────┘
         │ Saves to
         ▼
┌─────────────────┐
│ /videos/        │ 💾
│ laptop_camera_  │
│ latest.mp4      │
└────────┬────────┘
         │ Read by
         ▼
┌─────────────────┐
│ Backend API     │ Uploads to VLM
└────────┬────────┘
         │ Sends to
         ▼
┌─────────────────┐
│ Milestone VLM   │ 🤖 Analyzes
└────────┬────────┘
         │ Returns analysis
         ▼
┌─────────────────┐
│ Mobile Frontend │ 🔊 Speaks to user
└─────────────────┘
```

## Troubleshooting

### Camera not found
- Check your camera is connected
- Try different camera ID: `--camera 1` or `--camera 2`
- On Windows: Check Camera Privacy Settings

### Permission denied
- Allow camera access in your OS settings
- On macOS: System Preferences → Security & Privacy → Camera
- On Windows: Settings → Privacy → Camera

### Low FPS or quality
- Reduce resolution in `camera_server.py`:
  ```python
  self.frame_width = 640
  self.frame_height = 480
  ```

## Production Deployment

For a real CCTV camera deployment:

1. **Install on a dedicated machine** near the location
2. **Run as a service** (systemd on Linux, Windows Service)
3. **Use external camera** with better quality
4. **Add multiple cameras** - just run multiple instances with different camera IDs
5. **Add to camera registry** with actual GPS coordinates

Example systemd service (`/etc/systemd/system/loriens-camera.service`):
```ini
[Unit]
Description=Lórien's Guide Camera Server
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Loriens-Guide
ExecStart=/usr/bin/python3 camera_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable with:
```bash
sudo systemctl enable loriens-camera
sudo systemctl start loriens-camera
```
