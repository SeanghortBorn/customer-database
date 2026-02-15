from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Customer Database API", version="0.1.0")

# CORS - allow frontend origins
allowed_origins = [
    "http://localhost:3000",  # Local development
    "https://customer-database-system.vercel.app",  # Production frontend (Vercel)
]

# Add FRONTEND_URL from environment if set
frontend_url = os.getenv("FRONTEND_URL", "").strip()
if frontend_url and frontend_url not in allowed_origins:
    allowed_origins.append(frontend_url)

# Remove empty strings
allowed_origins = [origin for origin in allowed_origins if origin]

print("=" * 60)
print(f"🚀 Starting Customer Database API")
print(f"📍 CORS allowed origins: {allowed_origins}")
print(f"🔑 JWT_SECRET_KEY: {'✅ Set' if os.getenv('JWT_SECRET_KEY') else '❌ NOT SET'}")
print(f"🗄️  DATABASE_URL: {'✅ Set' if os.getenv('DATABASE_URL') else '❌ NOT SET'}")
print("=" * 60)

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
    """Comprehensive health check - tests database connection"""
    from shared.database import SessionLocal
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
    
    return health_status

@app.get("/")
async def root():
    return {"message": "Customer Database API v0.1.0"}

# Include routers
from services.auth.routes import router as auth_router
from services.workspace.routes import router as workspace_router
from services.list.routes import router as list_router
from services.item.routes import router as item_router
from services.relationship.routes import router as relationship_router
from services.audit.routes import router as audit_router

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(workspace_router, prefix="/api/v1", tags=["workspaces"])
app.include_router(list_router, prefix="/api/v1", tags=["lists"])
app.include_router(item_router, prefix="/api/v1", tags=["items"])
app.include_router(relationship_router, prefix="/api/v1", tags=["relationships"])
app.include_router(audit_router, prefix="/api/v1", tags=["audit"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)