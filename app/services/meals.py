from typing import List
from app.services.meal_templates import MEAL_TEMPLATES


def filter_meals(preferences: List[str], allergies: List[str], limit: int = 5):
    results = []

    for meal in MEAL_TEMPLATES:
        # Must satisfy all preferences
        if not all(pref in meal["tags"] for pref in preferences):
            continue

        # Hard exclusion for allergies (simple string match)
        if any(allergen.lower() in meal["name"].lower() for allergen in allergies):
            continue

        results.append(meal["name"])

        if len(results) >= limit:
            break

    return results
