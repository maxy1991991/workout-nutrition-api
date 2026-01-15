from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.db.models import Recommendation, User

from app.schemas.recommendation import RecommendationRequest

from app.services.nutrition import (
    calculate_bmr,
    calculate_tdee,
    adjust_calories,
    calculate_macros,
)
from app.services.workouts import generate_workout_plan
from app.services.meals import filter_meals



def generate_recommendation_output(payload: RecommendationRequest) -> dict:
    stats = payload.user_stats
    goals = payload.goals

    # Nutrition
    bmr = calculate_bmr(
        sex=stats.sex,
        weight_kg=stats.weight_kg,
        height_cm=stats.height_cm,
        age=stats.age,
    )
    tdee = calculate_tdee(bmr, stats.activity_level)
    calories = adjust_calories(tdee, goals.goal_type)
    macros = calculate_macros(calories, stats.weight_kg, goals.goal_type)

    # Workouts
    workout_plan = generate_workout_plan(
        training_days=goals.training_days_per_week,
        experience=goals.experience_level,
        equipment=stats.equipment,
    )

    # Meals
    meals = filter_meals(
        preferences=payload.dietary_restrictions.preferences,
        allergies=payload.dietary_restrictions.allergies,
    )

    return {
        "nutrition": macros,
        "workout_plan": workout_plan,
        "meals": meals,
    }

router = APIRouter(prefix="/v1", tags=["recommendations"])

@router.post("/recommendations")
def generate_recommendation(
    payload: RecommendationRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),):

    output = generate_recommendation_output(payload)

    rec = Recommendation(
        user_id=user.id,
        input_payload=payload.model_dump(),
        output_payload=output,
    )

    db.add(rec)
    db.commit()
    db.refresh(rec)

    return {
        "id": rec.id,
        **output,
    }

@router.get("/recommendations/{rec_id}")
def get_recommendation(
    rec_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == rec_id,
            Recommendation.user_id == user.id,
        )
        .first()
    )

    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return {
        "id": rec.id,
        "created_at": rec.created_at,
        **rec.output_payload,
    }

@router.get("/recommendations")
def list_recommendations(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    recs = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    return [
        {
            "id": rec.id,
            "created_at": rec.created_at,
        }
        for rec in recs
    ]


@router.put("/recommendations/{rec_id}")
def update_recommendation(
    rec_id: int,
    payload: RecommendationRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == rec_id,
            Recommendation.user_id == user.id,
        )
        .first()
    )

    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    output = generate_recommendation_output(payload)

    rec.input_payload = payload.model_dump()
    rec.output_payload = output

    db.commit()
    db.refresh(rec)

    return {
        "id": rec.id,
        **output,
    }


@router.delete("/recommendations/{rec_id}")
def delete_recommendation(
    rec_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == rec_id,
            Recommendation.user_id == user.id,
        )
        .first()
    )

    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    db.delete(rec)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
