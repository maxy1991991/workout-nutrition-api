from app.services.nutrition import (
    calculate_bmr,
    calculate_tdee,
    adjust_calories,
    calculate_macros,
)


def test_bmr_male():
    bmr = calculate_bmr("male", 70, 175, 25)
    assert round(bmr) == 1674


def test_tdee_moderate():
    tdee = calculate_tdee(1600, "moderate")
    assert round(tdee) == round(1600 * 1.55)


def test_calorie_adjustment():
    assert adjust_calories(2500, "fat_loss") == 2000
    assert adjust_calories(2500, "muscle_gain") == 2800
    assert adjust_calories(2500, "maintenance") == 2500


def test_macro_distribution():
    macros = calculate_macros(2500, 70, "muscle_gain")
    assert macros["protein_g"] > 0
    assert macros["fat_g"] > 0
    assert macros["carbs_g"] >= 0
