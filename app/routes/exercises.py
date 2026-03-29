from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import get_db
from app.models.workout import Exercise

router = APIRouter()


class ExerciseCreate(BaseModel):
    name: str
    category: Optional[str] = None
    muscle_group: Optional[str] = None
    description: Optional[str] = None


class ExerciseResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    muscle_group: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    if db.query(Exercise).filter(Exercise.name == exercise.name).first():
        raise HTTPException(status_code=400, detail="Exercise already exists")
    db_exercise = Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@router.get("/", response_model=List[ExerciseResponse])
def list_exercises(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Exercise)
    if category:
        query = query.filter(Exercise.category == category)
    return query.all()


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise
