from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.nutrition import NutritionLog

router = APIRouter()


class NutritionCreate(BaseModel):
    user_id: int
    food_name: str
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    meal_type: Optional[str] = None


class NutritionResponse(BaseModel):
    id: int
    user_id: int
    food_name: str
    calories: Optional[float]
    protein_g: Optional[float]
    carbs_g: Optional[float]
    fat_g: Optional[float]
    meal_type: Optional[str]
    date: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=NutritionResponse, status_code=status.HTTP_201_CREATED)
def log_nutrition(entry: NutritionCreate, db: Session = Depends(get_db)):
    db_entry = NutritionLog(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/user/{user_id}", response_model=List[NutritionResponse])
def get_user_nutrition(user_id: int, db: Session = Depends(get_db)):
    return db.query(NutritionLog).filter(NutritionLog.user_id == user_id).all()


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nutrition_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(NutritionLog).filter(NutritionLog.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
