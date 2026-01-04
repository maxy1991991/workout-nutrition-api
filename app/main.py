from fastapi import FastAPI
from app.api.recommendations import router as recommendations_router

app = FastAPI(title="Workout + Nutrition API")

app.include_router(recommendations_router)


@app.get("/health")
def health():
    return {"status": "ok"}
