from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import httpx

app = FastAPI()

# Requirement: Access-Control-Allow-Origin: *
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/classify")
async def classify_name(name: str = Query(None)):

    #  Validation: 400 Bad Request
    if not name or name.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": "Missing or empty name parameter"}
        )

    # Note: FastAPI handles the "is a string" check automatically
    # but i return 422 if it fails the internal validation.

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.genderize.io/?name={name}", timeout=5.0)

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail={"status": "error", "message": "Upstream API failure"})

        data = response.json()

        #  Genderize Edge Cases
        if data.get("gender") is None or data.get("count") == 0:
            return {
                "status": "error",
                "message": "No prediction available for the provided name"
            }

        #  Data Extraction & Logic
        probability = data.get("probability", 0.0)
        sample_size = data.get("count", 0)

        # Confidence Logic: probability >= 0.7 AND sample_size >= 100
        is_confident = (probability >= 0.7) and (sample_size >= 100)

        # ISO 8601 UTC Timestamp
        processed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        return {
            "status": "success",
            "data": {
                "name": name,
                "gender": data.get("gender"),
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"status": "error", "message": "Failed to connect to upstream API"}
        )