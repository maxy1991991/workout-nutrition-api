from math import floor

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}


def calculate_bmr(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    # Mifflin-St Jeor
    if sex == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_tdee(bmr: float, activity_level: str) -> float:
    return bmr * ACTIVITY_MULTIPLIERS[activity_level]


def adjust_calories(tdee: float, goal_type: str) -> int:
    if goal_type == "fat_loss":
        return floor(tdee - 500)
    if goal_type == "muscle_gain":
        return floor(tdee + 300)
    return floor(tdee)


def calculate_macros(
    calories: int,
    weight_kg: float,
    goal_type: str,
):
    # Protein
    protein_per_kg = 2.2 if goal_type == "muscle_gain" else 1.8
    protein_g = floor(weight_kg * protein_per_kg)

    # Fat
    fat_g = floor(weight_kg * 0.8)

    # Remaining calories → carbs
    protein_cal = protein_g * 4
    fat_cal = fat_g * 9
    remaining_cal = calories - (protein_cal + fat_cal)
    carbs_g = floor(max(remaining_cal / 4, 0))

    return {
        "calories": calories,
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_g": carbs_g,
    }
