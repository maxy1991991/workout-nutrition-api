from fastapi import FastAPI
from app.api.recommendations import router as recommendations_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Workout + Nutrition API")

app.include_router(recommendations_router)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}
