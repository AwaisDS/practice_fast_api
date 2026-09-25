from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from database import Base, engine, get_db


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

HTML_FILE = BASE_DIR / "templates" / "index.html"
STATIC_DIR = BASE_DIR / "static"


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="Student Management API",
    description="Student Management REST API with SQLite",
    version="1.0.0"
)


# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# ==========================================
# DATABASE MODEL
# ==========================================

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    department = Column(
        String,
        nullable=False
    )


# Create database tables
Base.metadata.create_all(bind=engine)


# ==========================================
# PYDANTIC MODEL
# ==========================================

class Student(BaseModel):
    name: str
    age: int
    department: str


# ==========================================
# FRONTEND
# ==========================================

@app.get("/")
def home():

    return FileResponse(HTML_FILE)


# ==========================================
# GET ALL STUDENTS
# ==========================================

@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(StudentDB).all()

    return students


# ==========================================
# GET STUDENT BY ID
# ==========================================

@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ==========================================
# ADD STUDENT
# ==========================================

@app.post("/students", status_code=201)
def add_student(
    student: Student,
    db: Session = Depends(get_db)
):

    new_student = StudentDB(
        name=student.name,
        age=student.age,
        department=student.department
    )

    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }


# ==========================================
# DELETE STUDENT
# ==========================================

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return {
        "message": "Student deleted successfully"
    }