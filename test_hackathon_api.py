"""Test script for Milestone Hackathon VLM API integration.

This script tests the complete workflow:
1. Upload a video asset
2. Send a chat completion request with the asset
3. Parse the response
4. Clean up by deleting the asset

Usage:
    python test_hackathon_api.py --video path/to/video.mp4
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from loriens_guide.vlm_service import VLMService

load_dotenv()


def test_asset_upload(service: VLMService, video_path: str) -> str | None:
    """Test uploading a video asset."""
    print(f"\n1. Uploading video asset: {video_path}")
    result = service.upload_video_asset(video_path)

    if "error" in result:
        print(f"   ❌ Upload failed: {result.get('message')}")
        return None

    asset_id = result.get("asset_id")
    print(f"   ✅ Upload successful! Asset ID: {asset_id}")
    return asset_id


def test_chat_completion(service: VLMService, asset_id: str) -> dict | None:
    """Test sending a chat completion request."""
    print("\n2. Sending chat completion request...")

    # System prompt with structured output guidance (per Hackathon docs)
    system_prompt = (
        "You are an accessibility assistant for vision-impaired users. "
        "Provide clear, concise guidance using landmarks and directional cues. "
        "Return a JSON object with 'guidance' and 'key_observations' fields."
    )

    # User prompt asking for navigation guidance
    user_prompt = (
        "Analyze this street view video. "
        "What obstacles or hazards should a vision-impaired person be aware of? "
        "Describe the safest path forward."
    )

    result = service.call_vlm_api(asset_id, user_prompt, system_prompt)

    if "error" in result:
        print(f"   ❌ Chat completion failed: {result.get('message')}")
        return None

    print("   ✅ Chat completion successful!")
    print("\n   Response:")
    response_text = result.get("text", "")
    print(f"   {response_text[:500]}...")  # Show first 500 chars

    return result


def test_asset_deletion(service: VLMService, asset_id: str) -> bool:
    """Test deleting a video asset."""
    print(f"\n3. Deleting asset: {asset_id}")
    success = service.delete_asset(asset_id)

    if success:
        print("   ✅ Asset deleted successfully")
    else:
        print("   ❌ Failed to delete asset")

    return success


def main() -> None:
    """Run the complete test workflow."""
    parser = argparse.ArgumentParser(description="Test Milestone Hackathon VLM API")
    parser.add_argument("--video", required=True, help="Path to video file (.mp4 or .mkv)")
    args = parser.parse_args()

    # Check if video file exists
    if not Path(args.video).exists():
        print(f"❌ Error: Video file not found: {args.video}")
        sys.exit(1)

    # Check if API credentials are set
    api_key = os.getenv("HACKATHON_API_KEY")
    api_secret = os.getenv("HACKATHON_API_SECRET")

    if not api_key or not api_secret:
        print("❌ Error: API credentials not found!")
        print("   Please set HACKATHON_API_KEY and HACKATHON_API_SECRET environment variables")
        print("   Or add them to a .env file")
        sys.exit(1)

    print("=" * 60)
    print("Milestone Hackathon VLM API Test")
    print("=" * 60)
    print(f"Video: {args.video}")
    print(f"API Key: {api_key[:8]}...{api_key[-4:]}")
    print(f"API Secret: {api_secret[:4]}...{api_secret[-4:]}")
    print("=" * 60)

    # Initialize service
    service = VLMService()

    # Test workflow
    asset_id = test_asset_upload(service, args.video)
    if not asset_id:
        sys.exit(1)

    result = test_chat_completion(service, asset_id)
    if not result:
        sys.exit(1)

    # Optional: Clean up
    cleanup = input("\n   Delete the asset now? (y/n): ").lower()
    if cleanup == "y":
        test_asset_deletion(service, asset_id)
    else:
        print(f"\n  ℹ️  Asset {asset_id} will be automatically purged after the hackathon")  # noqa: RUF001

    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
