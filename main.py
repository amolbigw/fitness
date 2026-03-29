from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import users, workouts, exercises, nutrition

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness App API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["workouts"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(nutrition.router, prefix="/api/nutrition", tags=["nutrition"])


@app.get("/")
def root():
    return {"message": "Fitness App API is running"}
