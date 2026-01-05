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
from app.services.meals import filter_meals

from app.services.workouts import generate_workout_plan
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.models import Recommendation
from app.db.deps import get_db

router = APIRouter(prefix="/v1", tags=["recommendations"])

@router.post("/recommendations")
def generate_recommendation(payload: RecommendationRequest,db: Session = Depends(get_db),):
    stats = payload.user_stats
    goals = payload.goals
    print (payload.goals)
    bmr = calculate_bmr(
        sex=stats.sex,
        weight_kg=stats.weight_kg,
        height_cm=stats.height_cm,
        age=stats.age,
    )
    tdee = calculate_tdee(bmr, stats.activity_level)
    calories = adjust_calories(tdee, goals.goal_type)
    macros = calculate_macros(calories, stats.weight_kg, goals.goal_type)
    
    workout_plan = generate_workout_plan(
        training_days=goals.training_days_per_week,
        experience=goals.experience_level,
        equipment=stats.equipment,
    )
    meals = filter_meals(preferences=payload.dietary_restrictions.preferences,allergies=payload.dietary_restrictions.allergies,)

    rec = Recommendation(
        input_payload=payload.model_dump(),
        output_payload={
            "nutrition": macros,
            "workout_plan": workout_plan,           
            "meals": meals,
        },
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return {
        "id": rec.id,
        "nutrition": macros,
        "workout_plan": workout_plan,
        "meals": meals,
        "notes": "Stored recommendation with reproducible inputs."
    }
@router.get("/recommendations/{rec_id}")
def get_recommendation(rec_id: int, db: Session = Depends(get_db)):
    rec = db.get(Recommendation, rec_id)
    if not rec:
        return {"error": "Recommendation not found"}

    return {
        "id": rec.id,
        "created_at": rec.created_at,
        **rec.output_payload,
    }



