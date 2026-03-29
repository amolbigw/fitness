from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String)  # strength, cardio, flexibility
    muscle_group = Column(String)
    description = Column(Text)

    workout_sets = relationship("WorkoutSet", back_populates="exercise")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    notes = Column(Text)
    duration_minutes = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")
    sets = relationship("WorkoutSet", back_populates="workout")


class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight_kg = Column(Float)
    duration_seconds = Column(Integer)  # for cardio/timed exercises

    workout = relationship("Workout", back_populates="sets")
    exercise = relationship("Exercise", back_populates="workout_sets")
