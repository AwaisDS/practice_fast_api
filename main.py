
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create the FastAPI application
app = FastAPI(title="Student Management API")


# Define the structure of a student
class Student(BaseModel):
    name: str
    age: int
    department: str


# Temporary database
students = [
    {
        "id": 1,
        "name": "Ahmed",
        "age": 21,
        "department": "Software Engineering"
    }
]


# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to Student API!"
    }


# GET: Get all students
@app.get("/students")
def get_students():
    return students


# GET: Get one student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# POST: Add a new student
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


# DELETE: Delete a student
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