# Workout + Nutrition Recommendation API

This project is a REST API that generates personalized workout plans and nutrition recommendations based on user inputs such as goals, experience level, available equipment, and dietary restrictions.

It also includes a simple web interface so the system can be tested without Swagger, Postman, or any external tools.

---

## What it does

Given a user profile, the API:
- calculates daily calorie and macronutrient targets
- generates a multi-day workout plan with sets, reps, and intensity
- filters meal templates based on dietary preferences and allergies
- stores recommendations in PostgreSQL
- associates each recommendation with a specific user account

---

## Key features

- FastAPI + Python
- PostgreSQL persistence using JSONB
- User authentication with email/password and JWT tokens
- Per-user data isolation (users can only access their own plans)
- Full CRUD support for workout and nutrition plans
- Experience-based training logic  

---

## Authentication and user accounts

The API supports basic user accounts using email and password authentication.

- Users can register and log in
- Login returns a JWT access token
- The token is required for all recommendation endpoints
- Each recommendation is owned by a single user
- Users cannot view, modify, or delete other users’ plans

Authentication is handled using standard JWT bearer tokens.

---

## CRUD functionality

Each authenticated user can fully manage their own plans:

- Create new workout and nutrition plans
- View a list of their existing plans
- Load a specific plan
- Update an existing plan using new inputs
- Delete a plan permanently

All CRUD operations are scoped to the logged-in user.

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

## Using the demo UI

The demo web page allows you to:

- register and log in as a user
- create new workout and nutrition plans
- view a list of your saved plans
- load an existing plan
- update a plan using modified inputs
- delete a plan
- log out and securely end the session

All requests from the UI use the same API endpoints that a real client would use.

---

## API endpoints

### Authentication

- POST /auth/register  
  Registers a new user with email and password.

- POST /auth/login  
  Logs in a user and returns a JWT access token.

---

### Recommendations (authenticated)

- POST /v1/recommendations  
  Creates and stores a new recommendation for the logged-in user.

- GET /v1/recommendations  
  Lists all recommendations belonging to the logged-in user.

- GET /v1/recommendations/{id}  
  Retrieves a specific recommendation owned by the user.

- PUT /v1/recommendations/{id}  
  Updates an existing recommendation using new input data.

- DELETE /v1/recommendations/{id}  
  Deletes a recommendation owned by the user.

All recommendation endpoints require a valid Authorization header with a bearer token.

## License

MIT
