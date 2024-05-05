import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {
        "name": "MD. Mehedi Hasan Maruf",
        "age": 22,
        "roll": 2003037
    },
    2: {
        "name": "Sadia Rahman Sharna",
        "age": 22,
        "roll": 2003009
    },
}


class Student(BaseModel):
    name: str
    age: int
    roll: int


@app.get("/")
def root():
    return {"Hello": "World"}


# variable path
@app.get("/items/{item_id}/{any_type_name}")
def read_item(item_id: int, any_type_name, q: str = None):
    return {"item_id": item_id, "Variable Type Parameters": any_type_name, "q": q}


# get all students
@app.get("/students")
async def get_students():
    # dict values can't be returned directly
    return list(students.values())

    # for passing names of students only
    # return [{"name": student["name"]} for student in students.values()]

    # remove roll only
    # return [{key: value for key, value in student.items() if key != "roll"} for student in students.values()]


# get student by id
@app.get("/students/{student_id}")
async def get_student_details(
        student_id: int = Path(
            ..., title="The ID of the student to get",
            description="Enter Student ID",
            ge=1,
            le=len(students)
        )
):
    return students[student_id]


# Get students by name (optional)
@app.get("/studentByName")
async def get_student_by_name(name: Optional[str] = None):
    if name is None:
        return students
    # gives all the students with the name
    result = [student for student in students.values() if name.lower()
              in student["name"].lower()]
    if result:
        return result
    return {"Data": "Not Found"}


@app.post("/students/{student_id}")
# required parameters can't be passed after optional parameters, so used *, in the beginning
def create_student(*, student: Optional[dict] = students, student_id: int):
    if student_id in students:
        return {"Error": "Student already exists"}

    students[student_id] = student
    return students[student_id]


if __name__ == "__main__":
    load_dotenv()
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    print(f"Starting server at {host}:{port}")
    uvicorn.run('main:app', host=host, port=port,
                log_level="info", reload=True)
