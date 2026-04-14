"""
app module

FastAPI application entrypoint.
Registers all routers and global middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routers import userRoutes, organisationRoutes, organisationApplicationRoutes, messageRoutes, authRoutes

app = FastAPI(
    title="Nkhunda Messaging API",
    description="A messaging API for managing organisations, applications, users and messages.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — adjust origins for your deployment environment
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict this list in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(authRoutes.router)
app.include_router(userRoutes.router)
app.include_router(organisationRoutes.router)
app.include_router(organisationApplicationRoutes.router)
app.include_router(messageRoutes.router)


@app.get("/", tags=["root"], include_in_schema=False)
async def read_root():
    """Redirect root to interactive API docs."""
    return RedirectResponse(url="/docs")