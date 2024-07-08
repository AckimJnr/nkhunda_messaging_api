from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from routers import userRoutes
from routers import organisationRoutes
from routers import organisationApplicationRoutes
from routers import messageRoutes
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
"""
App module entry point to server
"""

app = FastAPI()
router = APIRouter()


app.include_router(userRoutes.router)
app.include_router(organisationRoutes.router)
app.include_router(organisationApplicationRoutes.router)
app.include_router(messageRoutes.router)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return RedirectResponse(url="/docs")


app.include_router(router)