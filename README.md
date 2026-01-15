# Workout + Nutrition Recommendation API

This project is a small REST API that generates workout plans and nutrition recommendations based on user inputs like goals, experience level, available equipment, and dietary restrictions.

There’s also a simple web demo so you can test it quickly.

---

## What it does

Given a user profile, the API:
- calculates daily calorie and macro targets
- generates a multi-day workout plan with sets, reps, and intensity
- filters meal templates based on dietary preferences and allergies
- stores the recommendation in PostgreSQL so it can be retrieved later

---

## Key features

- FastAPI + Python
- PostgreSQL persistence using JSONB
- Experience-based training logic  
  Beginners receive higher volume to support motor learning and neural adaptation.  
  Advanced lifters receive lower volume with higher intensity due to diminishing coordination returns.
- Equipment-aware exercise selection  
  Bodyweight, dumbbells, or full gym setups are supported.
- Dietary restriction filtering  
  Gluten-free, lactose-free, vegetarian, vegan, and allergy-based exclusions.
- Reproducible recommendations  
  Every generated plan is stored and retrievable by ID.

---

## Quick start (local)

### 1. Create and activate a virtual environment (PowerShell)

    python -m venv .venv
    .venv\Scripts\Activate.ps1

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Create the database (PostgreSQL must be running)

    psql -U postgres

Inside psql:

    CREATE DATABASE workout_api;
    CREATE USER workout_user WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE workout_api TO workout_user;
    \q

### 4. Initialize tables

    python init_db.py

### 5. Run the server

    uvicorn app.main:app --reload

Open in a browser:

    http://127.0.0.1:8000

---

## Using the demo

The demo page allows you to:
- change body stats
- select training goal and equipment
- choose dietary preferences
- add allergies
- generate a recommendation
- reload a saved recommendation by ID

---

## API endpoints 

- POST /v1/recommendations  
  Generates and stores a new recommendation.

- GET /v1/recommendations/{id}  
  Retrieves a previously generated recommendation.

---

### Why higher volume for beginners?

The programming model assumes beginners benefit from higher volume due to neural adaptation and motor learning.  
Advanced lifters have less room for coordination gains and require tighter fatigue management.


