from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from routers import userRoutes, organisationRoutes, organisationApplicationRoutes, messageRoutes, authRoutes

app = FastAPI()
router = APIRouter()

app.include_router(authRoutes.router)
app.include_router(userRoutes.router)
app.include_router(organisationRoutes.router)
app.include_router(organisationApplicationRoutes.router)
app.include_router(messageRoutes.router)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return RedirectResponse(url="/docs")

app.include_router(router)