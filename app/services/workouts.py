from collections import defaultdict
from typing import List
from app.services.exercise_catalog import EXERCISES

MOVEMENT_PATTERNS = ["squat", "hinge", "push", "pull", "core"]
EQUIPMENT_ACCESS = {
    "bodyweight": {"bodyweight"},
    "dumbbell": {"bodyweight", "dumbbell"},
    "gym": {"bodyweight", "dumbbell", "gym"},
}
PROGRAMMING = {
    "beginner": {
        "sets": 5,
        "reps": "6-10",
        "intensity": "RPE 6-7"
    },
    "intermediate": {
        "sets": 4,
        "reps": "5-8",
        "intensity": "RPE 7-8"
    },
    "advanced": {
        "sets": 3,
        "reps": "3-6",
        "intensity": "RPE 8-9"
    },
}


def select_exercises(equipment: str) -> dict:
    allowed = EQUIPMENT_ACCESS[equipment]
    selected = defaultdict(list)

    for ex in EXERCISES:
        if ex["equipment"] in allowed:
            selected[ex["pattern"]].append(ex["name"])

    return selected


def generate_workout_plan(
    training_days: int,
    experience: str,
    equipment: str,
):
    exercises_by_pattern = select_exercises(equipment)
    programming = PROGRAMMING[experience]

    plan = []

    for day in range(training_days):
        day_exercises = []

        for pattern in MOVEMENT_PATTERNS:
            options = exercises_by_pattern.get(pattern, [])
            if not options:
                continue

            exercise_name = options[day % len(options)]

            day_exercises.append(
                {
                    "name": exercise_name,
                    "sets": programming["sets"],
                    "reps": programming["reps"],
                    "intensity": programming["intensity"],
                }
            )

        plan.append(
            {
                "day": f"Day {day + 1}",
                "focus": "Full Body",
                "exercises": day_exercises,
            }
        )

    return plan

