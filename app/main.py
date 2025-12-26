from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows   
from fastapi.openapi.utils import get_openapi
from app.api.notes import router as notes_router
from app.api.pa import router as pa_router
from app.api.auth import router as auth_router

# Modern lifespan handler (replaces on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" Backend started successfully")
    yield
    print("Backend shutting down")


app = FastAPI(
    title="LLM-Based Prior Authorization Form Generator",
    description="AI-assisted system for automating prior authorization workflows",
    version="1.0.0",
    lifespan=lifespan
)

# Routers
app.include_router(notes_router, prefix="/api/notes", tags=["Clinical Notes"])
app.include_router(pa_router, prefix="/api/pa", tags=["Prior Authorization"])
app.include_router(auth_router, prefix="/api")

# Health check
@app.get("/")
def health():
    return {"status": "Backend running"}


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
