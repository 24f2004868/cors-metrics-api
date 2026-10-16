
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uuid
import os

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-lr41x9.example.com"
USER_EMAIL = "24f2004868@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_headers(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response

@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        numbers = [int(x.strip()) for x in values.split(",")]
        if not numbers:
            raise ValueError
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "values must be comma-separated integers"},
        )

    return {
        "email": USER_EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }
