from pydantic import BaseModel, Field
from typing import List, Literal


class UserStats(BaseModel):
    age: int = Field(..., ge=13, le=100)
    sex: Literal["male", "female"]
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    activity_level: Literal[
        "sedentary",
        "light",
        "moderate",
        "active",
        "very_active",
    ]
    equipment: Literal["gym", "dumbbell", "bodyweight"]
    
class Goals(BaseModel):
    goal_type: Literal["fat_loss", "muscle_gain", "maintenance"]
    training_days_per_week: int = Field(..., ge=1, le=7)
    experience_level: Literal["beginner", "intermediate", "advanced"]

class DietaryRestrictions(BaseModel):
    allergies: List[str] = []
    preferences: List[
        Literal["gluten_free", "lactose_free", "vegetarian", "vegan"]
    ] = []


class RecommendationRequest(BaseModel):
    user_stats: UserStats
    goals: Goals
    dietary_restrictions: DietaryRestrictions


class NutritionTargets(BaseModel):
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int


class WorkoutDay(BaseModel):
    day: str
    focus: str
    exercises: List[str]


class RecommendationResponse(BaseModel):
    nutrition: NutritionTargets
    workout_plan: List[WorkoutDay]
    meals: List[str]
    notes: str

