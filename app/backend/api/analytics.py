from fastapi import APIRouter
from typing import List

router = APIRouter()

# Placeholder time-series data
revenue_data = [
    {"month": "Jan", "revenue": 1200},
    {"month": "Feb", "revenue": 2100},
    {"month": "Mar", "revenue": 800},
    {"month": "Apr", "revenue": 1600},
    {"month": "May", "revenue": 2400},
]
growth_data = [
    {"month": "Jan", "users": 30},
    {"month": "Feb", "users": 45},
    {"month": "Mar", "users": 60},
    {"month": "Apr", "users": 80},
    {"month": "May", "users": 120},
]
engagement_data = [
    {"month": "Jan", "engagement": 300},
    {"month": "Feb", "engagement": 500},
    {"month": "Mar", "engagement": 400},
    {"month": "Apr", "engagement": 700},
    {"month": "May", "engagement": 900},
]

@router.get("/revenue")
def get_revenue() -> List[dict]:
    return revenue_data

@router.get("/growth")
def get_growth() -> List[dict]:
    return growth_data

@router.get("/engagement")
def get_engagement() -> List[dict]:
    return engagement_data 