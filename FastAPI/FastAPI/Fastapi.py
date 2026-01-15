from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API is running"}

@app.get("/hello")
def hello():
    return {"message": "Hello, this is my first API"}

@app.get("/square/{num}")
def square(num: int):
    result = num * num
    return {"number": num, "square": result}

class Student(BaseModel):
    name: str
    age: int

@app.post("/add-student")
def add_student(student: Student):
    return {
        "msg": "Student added successfully",
        "student_data": student
    }
