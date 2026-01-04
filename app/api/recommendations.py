from fastapi import APIRouter
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    NutritionTargets,
    WorkoutDay,
)
from app.services.nutrition import (
    calculate_bmr,
    calculate_tdee,
    adjust_calories,
    calculate_macros,
)

router = APIRouter(prefix="/v1", tags=["recommendations"])


@router.post("/recommendations", response_model=RecommendationResponse)
def generate_recommendation(payload: RecommendationRequest):
    stats = payload.user_stats
    goals = payload.goals

    bmr = calculate_bmr(
        sex=stats.sex,
        weight_kg=stats.weight_kg,
        height_cm=stats.height_cm,
        age=stats.age,
    )
    tdee = calculate_tdee(bmr, stats.activity_level)
    calories = adjust_calories(tdee, goals.goal_type)
    macros = calculate_macros(calories, stats.weight_kg, goals.goal_type)

    return RecommendationResponse(
        nutrition=NutritionTargets(**macros),
        workout_plan=[
            WorkoutDay(
                day="Day 1",
                focus="Full Body",
                exercises=["Squat", "Bench Press", "Row"],
            )
        ],
        notes="Calories and macros calculated using Mifflin-St Jeor.",
    )
