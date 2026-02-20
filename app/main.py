import os

from fastapi import FastAPI

from app.routers.api import router as api_router

app = FastAPI()

app.include_router(api_router)

static_dir = os.path.join(os.path.dirname(__file__), "static")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "API is running"}
