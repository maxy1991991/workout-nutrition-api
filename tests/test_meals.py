from app.services.meals import filter_meals


def test_vegan_filter():
    meals = filter_meals(preferences=["vegan"], allergies=[])
    assert all("Tofu" in meal or "Vegan" in meal for meal in meals)


def test_lactose_free_filter():
    meals = filter_meals(preferences=["lactose_free"], allergies=["yogurt"])
    assert all("Yogurt" not in meal for meal in meals)


def test_limit():
    meals = filter_meals(preferences=[], allergies=[], limit=2)
    assert len(meals) == 2
