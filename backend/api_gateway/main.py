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
    """Basic health check"""
    return {"status": "ok", "service": "api"}

@app.get("/health/full")
async def health_full():
    """Comprehensive health check - tests database and Supabase connections"""
    from shared.database import SessionLocal
    from shared.auth import get_supabase_client
    from sqlalchemy import text
    
    health_status = {
        "status": "ok",
        "service": "api",
        "checks": {}
    }
    
    # Check database connection
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health_status["checks"]["database"] = {"status": "ok", "message": "Connected"}
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = {"status": "error", "message": str(e)}
    
    # Check Supabase connection
    try:
        supabase = get_supabase_client()
        # Simple check to see if client is initialized
        health_status["checks"]["supabase"] = {"status": "ok", "message": "Client initialized"}
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["supabase"] = {"status": "error", "message": str(e)}
    
    return health_status

@app.get("/")
async def root():
    return {"message": "Customer Database API v0.1.0"}

# Include routers
from services.workspace.routes import router as workspace_router
from services.list.routes import router as list_router
from services.item.routes import router as item_router
from services.relationship.routes import router as relationship_router
from services.audit.routes import router as audit_router

app.include_router(workspace_router, prefix="/api/v1", tags=["workspaces"])
app.include_router(list_router, prefix="/api/v1", tags=["lists"])
app.include_router(item_router, prefix="/api/v1", tags=["items"])
app.include_router(relationship_router, prefix="/api/v1", tags=["relationships"])
app.include_router(audit_router, prefix="/api/v1", tags=["audit"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)