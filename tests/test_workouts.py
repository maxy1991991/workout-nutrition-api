from app.services.workouts import generate_workout_plan


def test_workout_day_count():
    plan = generate_workout_plan(training_days=3)
    assert len(plan) == 3


def test_each_day_has_exercises():
    plan = generate_workout_plan(training_days=2)
    for day in plan:
        assert len(day["exercises"]) > 0


def test_deterministic_output():
    plan1 = generate_workout_plan(3)
    plan2 = generate_workout_plan(3)
    assert plan1 == plan2
