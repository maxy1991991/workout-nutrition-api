from fastapi import APIRouter
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    NutritionTargets,
    WorkoutDay,
)

router = APIRouter(prefix="/v1", tags=["recommendations"])


@router.post("/recommendations", response_model=RecommendationResponse)
def generate_recommendation(payload: RecommendationRequest):
    # TEMP stub response
    return RecommendationResponse(
        nutrition=NutritionTargets(
            calories=2200,
            protein_g=150,
            carbs_g=250,
            fat_g=70,
        ),
        workout_plan=[
            WorkoutDay(
                day="Day 1",
                focus="Full Body",
                exercises=["Squat", "Bench Press", "Row"],
            )
        ],
        notes="Stub response. Logic coming next.",
    )
