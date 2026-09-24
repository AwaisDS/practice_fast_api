from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


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
    description="Student Management REST API",
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
# STUDENT MODEL
# ==========================================

class Student(BaseModel):
    name: str
    age: int
    department: str


# ==========================================
# TEMPORARY DATABASE
# ==========================================

students = [
    {
        "id": 1,
        "name": "Ahmed",
        "age": 21,
        "department": "Software Engineering"
    }
]


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
def get_students():

    return students


# ==========================================
# GET STUDENT BY ID
# ==========================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:

        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# ==========================================
# ADD STUDENT
# ==========================================

@app.post("/students", status_code=201)
def add_student(student: Student):

    new_id = max(
        [s["id"] for s in students],
        default=0
    ) + 1

    new_student = {
        "id": new_id,
        **student.model_dump()
    }

    students.append(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }


# ==========================================
# DELETE STUDENT
# ==========================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:

        if student["id"] == student_id:

            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )