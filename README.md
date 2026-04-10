# Gender Classifier API - Stage 0

A simple, high-performance API that predicts the gender of a given name using the Genderize.io API. Built for the Stage 0 Backend Task.

## Tech Stack
- **Language:** Python 3.x
- **Framework:** FastAPI
- **HTTP Client:** Httpx (Async)
- **Deployment:** Railway / Vercel (or your chosen platform)

## Features
- **Data Transformation:** Maps external API data to a structured response.
- **Confidence Logic:** Automatically determines if a prediction is confident based on probability (≥ 0.7) and sample size (≥ 100).
- **CORS Enabled:** Supports cross-origin requests for grading and integration.
- **Error Handling:** Gracefully handles missing parameters, invalid names, and upstream API failures.

## API Specification

### Classify Name
**Endpoint:** `GET /api/classify?name={name}`

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "name": "mahfuz",
    "gender": "male",
    "probability": 0.97,
    "sample_size": 3715,
    "is_confident": true,
    "processed_at": "2026-04-10T14:29:30Z"
  }
}