from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router

app = FastAPI(
    title="AI Document Intelligence Agent",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)