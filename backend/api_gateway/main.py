from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Customer Database API", version="0.1.0")

# CORS - allow frontend origins
allowed_origins = [
    "http://localhost:3000",  # Local development
    os.getenv("FRONTEND_URL", ""),  # Production frontend
]
# Remove empty strings
allowed_origins = [origin for origin in allowed_origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Customer Database API v0.1.0"}

# Include routers as we build them
# from services.workspace.routes import router as workspace_router
# app.include_router(workspace_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)