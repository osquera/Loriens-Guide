from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Lórien's Guide API")


class GuidanceRequest(BaseModel):
    """Request model for guidance endpoint."""
    latitude: float
    longitude: float
    question_text: str


class GuidanceResponse(BaseModel):
    """Response model for guidance endpoint."""
    answer_text: str


@app.post("/api/get-guidance", response_model=GuidanceResponse)
async def get_guidance(request: GuidanceRequest):
    """
    Provide guidance based on location and user question.
    
    Args:
        request: GuidanceRequest containing latitude, longitude, and question_text
        
    Returns:
        GuidanceResponse with answer_text
    """
    # TODO: Implement actual logic to call Hafnia API and process guidance
    # For now, return a placeholder response
    answer = f"You are at coordinates ({request.latitude}, {request.longitude}). " \
             f"Regarding your question: '{request.question_text}' - " \
             f"You are facing the main hall. The exit is 20 steps forward, " \
             f"just past the large red sculpture on your left."
    
    return GuidanceResponse(answer_text=answer)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Lórien's Guide API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
