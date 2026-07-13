from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router
from api.dashboard_routes import router as dashboard_router
from api.dashboard_chat import router as chat_router

app = FastAPI(
    title="AI Document Intelligence Agent",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
app.include_router(dashboard_router)
app.include_router(chat_router)