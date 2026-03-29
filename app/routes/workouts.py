from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.workout import Workout, WorkoutSet

router = APIRouter()


class WorkoutSetCreate(BaseModel):
    exercise_id: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight_kg: Optional[float] = None
    duration_seconds: Optional[int] = None


class WorkoutCreate(BaseModel):
    user_id: int
    name: str
    notes: Optional[str] = None
    duration_minutes: Optional[int] = None
    sets: Optional[List[WorkoutSetCreate]] = []


class WorkoutSetResponse(BaseModel):
    id: int
    exercise_id: int
    sets: Optional[int]
    reps: Optional[int]
    weight_kg: Optional[float]
    duration_seconds: Optional[int]

    class Config:
        from_attributes = True


class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    name: str
    notes: Optional[str]
    duration_minutes: Optional[int]
    date: datetime
    sets: List[WorkoutSetResponse]

    class Config:
        from_attributes = True


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(
        user_id=workout.user_id,
        name=workout.name,
        notes=workout.notes,
        duration_minutes=workout.duration_minutes,
    )
    db.add(db_workout)
    db.flush()

    for s in workout.sets:
        db_set = WorkoutSet(workout_id=db_workout.id, **s.model_dump())
        db.add(db_set)

    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.get("/user/{user_id}", response_model=List[WorkoutResponse])
def get_user_workouts(user_id: int, db: Session = Depends(get_db)):
    return db.query(Workout).filter(Workout.user_id == user_id).all()


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
