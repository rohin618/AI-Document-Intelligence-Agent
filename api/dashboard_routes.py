from fastapi import APIRouter

from utils.analytics.analytics import get_dashboard_data

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard_home():
    return {
        "message": "Dashboard API is running."
    }


@router.get("/data")
def dashboard_data():
    return get_dashboard_data()