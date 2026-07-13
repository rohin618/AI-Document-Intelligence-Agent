from fastapi import APIRouter
from pydantic import BaseModel

from utils.analytics.analytics import get_dashboard_data
from utils.dashboard_chat.dashboard_chat import ask_dashboard_ai

router = APIRouter()

class ChatRequest(BaseModel):
    question: str


@router.post("/dashboard-chat")
def dashboard_chat(request: ChatRequest):

    dashboard = get_dashboard_data()

    answer = ask_dashboard_ai(
        dashboard,
        request.question
    )

    return {
        "answer": answer
    }