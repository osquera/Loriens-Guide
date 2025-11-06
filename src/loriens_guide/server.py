import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Lórien's Guide API")


class GuidanceRequest(BaseModel):
    """Request model for guidance endpoint."""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")
    question_text: str = Field(..., min_length=1, description="User's question about navigation")


class GuidanceResponse(BaseModel):
    """Response model for guidance endpoint."""

    answer_text: str


@app.post("/api/get-guidance")
async def get_guidance(request: GuidanceRequest) -> GuidanceResponse:
    """Provide guidance based on location and user question.

    Args:
        request: GuidanceRequest containing latitude, longitude, and question_text

    Returns:
        GuidanceResponse with answer_text

    """
    # TODO: Integrate with Hafnia API for actual guidance
    # Expected integration steps:
    # 1. Send location (latitude, longitude) and question to Hafnia API
    # 2. Receive spatial/navigation data and context from Hafnia
    # 3. Process the response to generate human-friendly directions
    # 4. Handle API errors and edge cases (out of bounds, unknown location, etc.)
    # For now, return a placeholder response
    answer = (
        f"You are at coordinates ({request.latitude}, {request.longitude}). "
        f"Regarding your question: '{request.question_text}' - "
        f"You are facing the main hall. The exit is 20 steps forward, "
        f"just past the large red sculpture on your left."
    )

    return GuidanceResponse(answer_text=answer)


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "Lórien's Guide API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
