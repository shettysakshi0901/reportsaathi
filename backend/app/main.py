
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, value
from .models.database import Base, engine


app = FastAPI(title="ReportSaathi Backend")

# Initialize database tables
Base.metadata.create_all(bind=engine)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(health.router, prefix="/api")
app.include_router(value.router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    return JSONResponse({
        "message": "ReportSaathi Backend is running"
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000"))
    )
