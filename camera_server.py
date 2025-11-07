"""Camera Server - Captures video from laptop webcam and serves it as a "CCTV camera".

This simulates a public camera feed for the Lórien's Guide system.

Usage:
    python camera_server.py

The server will:
1. Capture video from your laptop webcam
2. Save video clips periodically (e.g., 5-second clips)
3. Make the latest clip available for VLM analysis
"""

import time
from datetime import datetime
from pathlib import Path

import cv2


class CameraServer:
    def __init__(self, camera_id: int = 0, clip_duration: int = 5):
        """Initialize the camera server.

        Args:
            camera_id: Camera device ID (0 for default laptop webcam)
            clip_duration: Duration of each video clip in seconds
        """
        self.camera_id = camera_id
        self.clip_duration = clip_duration
        self.output_dir = Path(__file__).parent.parent / "videos"
        self.output_dir.mkdir(exist_ok=True)

        # Video settings
        self.fps = 30
        self.frame_width = 1280
        self.frame_height = 720

        # Initialize camera
        self.cap = None

    def start_camera(self):
        """Start capturing from the camera."""
        print(f"🎥 Starting camera {self.camera_id}...")
        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {self.camera_id}")

        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        print(f"✅ Camera opened successfully")
        print(
            f"   Resolution: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
        )
        print(f"   FPS: {self.cap.get(cv2.CAP_PROP_FPS)}")

    def capture_clip(self, output_filename: str) -> Path:
        """Capture a video clip of specified duration.

        Args:
            output_filename: Name of the output video file

        Returns:
            Path to the saved video clip
        """
        output_path = self.output_dir / output_filename

        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.frame_width, self.frame_height))

        print(f"📹 Recording {self.clip_duration}s clip to {output_filename}...")

        start_time = time.time()
        frame_count = 0

        while (time.time() - start_time) < self.clip_duration:
            ret, frame = self.cap.read()

            if not ret:
                print("⚠️  Failed to read frame")
                break

            # Resize if needed
            frame = cv2.resize(frame, (self.frame_width, self.frame_height))

            # Write frame
            out.write(frame)
            frame_count += 1

            # Optional: Display preview (comment out for headless operation)
            cv2.imshow("Camera Feed (Press Q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        out.release()

        print(f"✅ Captured {frame_count} frames ({frame_count / self.fps:.1f}s)")
        return output_path

    def run_continuous(self):
        """Run the camera server continuously, updating the video clip."""
        try:
            self.start_camera()

            print("\n" + "=" * 60)
            print("🎥 CAMERA SERVER RUNNING")
            print("=" * 60)
            print(f"Output directory: {self.output_dir}")
            print(f"Clip duration: {self.clip_duration}s")
            print(f"Press Ctrl+C to stop or Q in preview window")
            print("=" * 60 + "\n")

            clip_number = 0

            while True:
                # Use timestamp for filename to always have the latest
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"laptop_camera_{timestamp}.mp4"

                # Also keep a "latest" version for easy access
                latest_filename = "laptop_camera_latest.mp4"

                # Capture clip
                clip_path = self.capture_clip(filename)

                # Copy to "latest" for easy backend access
                import shutil

                latest_path = self.output_dir / latest_filename
                shutil.copy(clip_path, latest_path)

                clip_number += 1
                print(f"📦 Clip #{clip_number} saved: {filename}")
                print(f"   Latest clip available at: {latest_filename}")
                print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                print()

                # Small delay before next clip
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n⏹️  Stopping camera server...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Release camera and close windows."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Camera server stopped")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Camera Server for Lórien's Guide")
    parser.add_argument("--camera", type=int, default=0, help="Camera device ID (default: 0)")
    parser.add_argument("--duration", type=int, default=5, help="Clip duration in seconds (default: 5)")
    args = parser.parse_args()

    server = CameraServer(camera_id=args.camera, clip_duration=args.duration)
    server.run_continuous()
