from typing import Type
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uuid

id = uuid.uuid1().int

app= FastAPI()


ListOfStudent = []

class Student(BaseModel):
    id = id
    name: str
    gender: str
    major: str

class SecStudent(BaseModel):
    id : int
    name: Optional[str]=None
    gender: Optional[str]=None
    major: Optional[str]=None

@app.post("/addstudent/")
def add_new_student(student:Student):
    ListOfStudent.append(student)
    return {"data":f"{student.name} has been added"}

@app.get("/getstudents")
def get_student(gender : Optional[str] = None, major : Optional[str] = None):
    if gender == None and major == None :
        return ListOfStudent
    if gender and major == None:
        return [x for x in ListOfStudent if x.gender == gender]
    if major and gender == None:
        return [x for x in ListOfStudent if x.major == major]
    if major and gender :
        return [x for x in ListOfStudent if x.major == major and x.gender == gender]

@app.get("/getstudentbyid/{id}")
def  get_student_by_id(id:int):
    return [x for x in ListOfStudent if x.id == id]

@app.delete("/deletestudent")
def delete_student(id:int):
    for i in range(len(ListOfStudent)):
        print(ListOfStudent[i].id)
        if ListOfStudent[i].id == id:
            ListOfStudent.pop(i)
            break
    return {"data":"deleted"}

@app.put("/putstudent")
def put_student(student:Student):
    for i in range(len(ListOfStudent)):
            if ListOfStudent[i].id == student.id:
                ListOfStudent.pop(i)
                break
    ListOfStudent.append({
    "name": student.name,
    "gender": student.gender,
    "major": student.major,
    "id": student.id,
    })
    return {"data":f"{student.name} profile has been updater"}

@app.patch("/patchstudent")
def patch_student(student:SecStudent):
    for i in range(len(ListOfStudent)):
        if ListOfStudent[i].id == student.id:
            if student.name !=None:
                ListOfStudent[i].name=student.name
            if student.gender !=None:
                ListOfStudent[i].gender=student.gender
            if student.major != None:
                ListOfStudent[i].major=student.major
            break
    return{"data":"prfile hase been updated"}
