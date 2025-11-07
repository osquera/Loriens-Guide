# Milestone Hackathon API Integration Guide

## Overview

Lórien's Guide now integrates with the **Milestone Hackathon VLM API** (powered by NVIDIA Cosmos-Reason1). This document explains how to use the API for video analysis and accessibility guidance.

## API Specifications

- **Base URL**: `https://api.mdi.milestonesys.com`
- **Authentication**: `ApiKey <KEY>:<SECRET>` header format
- **OpenAPI Docs**: https://api.mdi.milestonesys.com/api/v1/vlm-docs (participants only)

## Video Requirements

- **Formats**: `.mp4` or `.mkv`
- **Max file size**: 100 MB
- **Duration**: <30 seconds (mandatory), ~15 seconds optimal
- **Resolution**: Up to ~1920px width (effective processing)
- **Audio**: Ignored by the service
- **Auto-processing**: Service transcodes/downsamples if needed

## Setup

### 1. Get API Credentials

Obtain your API credentials from the Hackathon organizers:
- `HACKATHON_API_KEY`
- `HACKATHON_API_SECRET`

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Milestone Hackathon API Configuration
HACKATHON_API_KEY=your_api_key_here
HACKATHON_API_SECRET=your_api_secret_here
VLM_API_URL=https://api.mdi.milestonesys.com

# Backend Configuration
PORT=5000
FLASK_DEBUG=false
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## API Workflow

The Hackathon API uses a **three-step process**:

### Step 1: Upload Video Asset

Upload your video file to get an `asset_id`:

```python
from loriens_guide.vlm_service import VLMService

service = VLMService()
result = service.upload_video_asset("path/to/video.mp4")
asset_id = result["asset_id"]
```

**API Call:**
```bash
POST /api/v1/assets
Content-Type: multipart/form-data
Authorization: ApiKey <KEY>:<SECRET>

file=@video.mp4
```

**Response:**
```json
{
  "asset_id": "41aefe6a-45b9-46c9-aef8-a3c21f451a9c",
  "status": "uploaded"
}
```

### Step 2: Send Chat Completion Request

Send a chat completion with the asset_id:

```python
system_prompt = "You are an accessibility assistant. Return clear guidance with landmarks."
user_prompt = "What obstacles should a vision-impaired person avoid in this video?"

result = service.call_vlm_api(asset_id, user_prompt, system_prompt)
print(result["text"])
```

**API Call:**
```bash
POST /api/v1/chat/completions
Content-Type: application/json
Authorization: ApiKey <KEY>:<SECRET>

{
  "messages": [
    {
      "role": "system",
      "content": [
        {"type": "text", "text": "Return clear guidance with landmarks."}
      ]
    },
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What obstacles should a vision-impaired person avoid?"},
        {"type": "asset_id", "asset_id": "41aefe6a-45b9-46c9-aef8-a3c21f451a9c"}
      ]
    }
  ]
}
```

**Response:**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "In this video, a vision-impaired person should be aware of..."
      }
    }
  ]
}
```

### Step 3: Delete Asset (Optional)

Clean up by deleting the asset:

```python
service.delete_asset(asset_id)
```

**API Call:**
```bash
DELETE /api/v1/assets/{asset_id}
Authorization: ApiKey <KEY>:<SECRET>
```

**Note**: All assets are automatically purged after the hackathon.

## Prompting Best Practices

### General Tips

1. **Be specific about time spans**: "Between 00:12–00:27 seconds..."
   - Time spans only work if provided in the **system prompt**
2. **Provide context**: Camera semantics, thresholds, policies
3. **Request structured output**: Ask for JSON with specific fields
4. **Use reasoning sections**: Encourage `<think>...</think>` and `<answer>` sections

### Recommended Prompt Size

- Keep ≤ ~500 tokens total input for reliability
- Most use cases need far less

### Template Examples

#### Alert Validation (Binary + Reason)

**System Prompt:**
```
Follow exactly this JSON schema; if uncertain use "uncertain".
<format>
{
  "verdict": "true|false|uncertain",
  "reason": "...",
  "time_spans": [{"start_s": float, "end_s": float}]
}
</format>
```

**User Prompt:**
```
Validate the {ALERT_TYPE} alert in this clip between {T0}-{T1} seconds.
Explain briefly. Cite frame/time spans.
```

#### Accessibility Guidance (Lórien's Guide)

**System Prompt:**
```
You are an accessibility assistant for vision-impaired users.
Provide clear, concise guidance using:
- Landmarks (not colors)
- Directional cues ("on your left", "ahead 10 steps")
- Time-coded observations
Return JSON: {"guidance": "...", "obstacles": [...], "safe_path": "..."}
```

**User Prompt:**
```
Analyze this street view from timestamp {START} to {END}.
What obstacles should a vision-impaired person avoid?
Describe the safest path forward with step-by-step directions.
```

#### Status Report

**System Prompt:**
```
Produce concise bullet points with time-codes, then a final JSON.
JSON keys: traffic_flow, incidents, obstructions, vulnerable_users, notable_behaviors.
```

**User Prompt:**
```
Create a situation report for {AREA} using the video.
```

## Testing

Run the test script to verify your API integration:

```bash
python test_hackathon_api.py --video path/to/your/video.mp4
```

This will:
1. Upload the video asset
2. Send a chat completion request
3. Display the response
4. Optionally delete the asset

## Integration Patterns

### Real-time Alert Validation

1. Analytics raises an alert
2. Export a 10-20 second clip
3. Upload + chat completion with validation prompt
4. Use verdict to escalate/close via XProtect Events API

### Automated City Status Reports

1. Sample short clips on a schedule
2. Batch upload + completions
3. Store JSON responses
4. Display on dashboards

### Assisted Incident Triage

1. Operator bookmarks a segment
2. One-click "Explain" button
3. VLM returns 5-bullet summary with time-codes

## Synchronous Processing

- **No webhooks**: Completions are synchronous
- **Wait for response**: Send next request after prior one returns
- **Throttling**: Dynamic throttling may apply under heavy load
- **Retry logic**: Back off on HTTP 429/5xx errors

## Error Handling

The VLM service includes comprehensive error handling:

```python
result = service.call_vlm_api(asset_id, user_prompt)

if "error" in result:
    print(f"Error: {result['message']}")
    print(f"Status: {result.get('status_code')}")
else:
    print(f"Success: {result['text']}")
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Upload fails | File >100MB or >30s | Trim video, reduce resolution |
| Response truncated | Prompt too complex | Simplify system prompt |
| Temporal references off | Video too long | Trim to relevant window, use explicit time ranges |
| HTTP 429 | Rate limiting | Back off, retry with exponential delay |
| Timeout | Long video processing | Use shorter clips (~15s optimal) |

## Structured Output

You can request strict JSON output, but note:
- **Not perfectly deterministic**: Always validate before parsing
- **Use schemas**: Provide exact JSON format in system prompt
- **Handle uncertainty**: Include "uncertain" as a valid value for classifications

Example validation:

```python
import json

result = service.call_vlm_api(asset_id, user_prompt, system_prompt)
response_text = result.get("text", "")

try:
    # Extract JSON from response (may be wrapped in markdown)
    json_start = response_text.find("{")
    json_end = response_text.rfind("}") + 1
    json_str = response_text[json_start:json_end]
    
    data = json.loads(json_str)
    print(f"Parsed: {data}")
except json.JSONDecodeError:
    print("Warning: Could not parse JSON, using raw text")
    print(response_text)
```

## Privacy & Data Handling

- **No organizer-provided data**: You must ensure rights & compliance for footage used
- **Audio ignored**: Content filters (faces, license plates) are your responsibility
- **Temporary storage**: Assets stored only for processing
- **Auto-deletion**: All data removed after hackathon
- **Manual deletion**: Use DELETE endpoint to remove assets anytime
- **Processing region**: US servers

## Responsible AI Guidelines

1. **Ensure data rights**: Only use footage you have permission to process
2. **Privacy protection**: Blur faces/plates if needed before upload
3. **Bias awareness**: Test with diverse scenarios and user groups
4. **Accessibility first**: Design for users with various abilities
5. **Transparent limitations**: Inform users of AI limitations

## XProtect Integration (Optional)

If integrating with Milestone XProtect VMS:

- **Events REST API**: Trigger/consume events
- **Events & State WebSocket**: Realtime subscriptions
- **Documentation**: See Hackathon resources

## Resources

- **Cosmos-Reason1 Evaluation Guide**: Evaluation flow documentation
- **Cosmos-Reason1 Model Card**: Output tokens & timestamp notes
- **Cosmos-Reason1 GitHub**: https://github.com/NVIDIA/Cosmos (overview)
- **XProtect Events REST API**: Events API documentation
- **XProtect WebSocket API**: Events/State WebSocket documentation

## Support

For Hackathon-specific support:
- Check the OpenAPI documentation: https://api.mdi.milestonesys.com/api/v1/vlm-docs
- Contact Hackathon organizers
- Review troubleshooting section above

## Example: Full Workflow

```python
from loriens_guide.vlm_service import VLMService

# Initialize service (reads API credentials from environment)
service = VLMService()

# 1. Upload video
video_path = "videos/intersection_example.mp4"
upload_result = service.upload_video_asset(video_path)

if "error" in upload_result:
    print(f"Upload failed: {upload_result['message']}")
    exit(1)

asset_id = upload_result["asset_id"]
print(f"Uploaded asset: {asset_id}")

# 2. Analyze with VLM
system_prompt = """
You are an accessibility assistant. Analyze videos to help vision-impaired users navigate safely.
Return JSON with these exact fields:
{
  "obstacles": ["list of obstacles with locations"],
  "safe_path": "step-by-step directions",
  "time_codes": [{"event": "...", "start_s": 0.0, "end_s": 5.0}]
}
"""

user_prompt = """
Analyze this intersection video from a vision-impaired user's perspective.
Identify obstacles, hazards, and provide clear navigation guidance.
Focus on the timespan 0:00 to 0:15.
"""

result = service.call_vlm_api(asset_id, user_prompt, system_prompt)

if "error" in result:
    print(f"Analysis failed: {result['message']}")
else:
    print("Analysis complete:")
    print(result["text"])

# 3. Clean up
service.delete_asset(asset_id)
print("Asset deleted")
```

## Production Deployment

For deploying your Hackathon project:

1. **Frontend**: Deploy to Cloudflare Pages (see `CLOUDFLARE_DEPLOYMENT.md`)
2. **Backend**: Deploy to Railway, Render, or Fly.io
3. **Environment Variables**: Set in deployment platform
4. **Video Storage**: Use cloud storage (S3, Cloudflare R2) for user-uploaded videos
5. **Caching**: Cache VLM responses to reduce API calls
6. **Rate Limiting**: Implement client-side rate limiting
7. **Error Handling**: Display user-friendly error messages

## Judging Criteria

Your project will be evaluated on:

1. **Potential value/impact**: Does it solve a real problem?
2. **Creativity**: Novel use of the VLM API
3. **Technical execution**: Clean architecture, proper error handling
4. **Functionality & scalability**: Does it work reliably?
5. **Demo quality**: Clear demonstration of features

## Submission Package

Submit:
- ✅ Application (working integration using VLM API)
- ✅ Text description (features, workflow, VLM usage)
- ✅ Demo video (≤3 minutes, YouTube/Vimeo link)
- ✅ Optional: Source code repo, live demo link, documentation

---

**Good luck with your Hackathon project! 🚀**
