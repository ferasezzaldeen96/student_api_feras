from fastapi import FastAPI, status, HTTPException
from typing import Optional
from uuid import uuid4
from models import PatchStudent, PostStudent, PutStudent, StudentResponse
from session import JSONResponse


app= FastAPI()


ListOfStudent = [
    StudentResponse(
        id=1,
        name= "feras",
        major= "software developer",
        gender= "male"
    ),
    StudentResponse(
        id=2,
        name= "sara",
        major= "manager",
        gender= "female"
    )
]


@app.get("/students")
def get_student(gender : Optional[str] = None, major : Optional[str] = None) -> JSONResponse:
    target = []
    if not gender and not major :
        target= ListOfStudent
    if gender and not major:
        target= [x for x in ListOfStudent if x.gender == gender]
    if major and not gender:
        target= [x for x in ListOfStudent if x.major == major]
    if major and gender :
        target= [x for x in ListOfStudent if x.major == major and x.gender == gender]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "data":target
        }
    )

@app.post("/addstudent")
def add_new_student(student: PostStudent) ->  JSONResponse:
    try :
        new_student = PostStudent(id=uuid4().int, **student.dict(exclude_none=True))
        ListOfStudent.append(new_student)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data":new_student
            }
    )
    except Exception as e:
        return {f"error{e}"}




@app.get("/getstudentbyid/{id}")
def  get_student_by_id(id:int) -> JSONResponse:
    target= [x for x in ListOfStudent if x.id == id]
    if target !=[]:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data":target
            }
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Student with id: {id} is not found'
    )

@app.delete("/deletestudent")
def delete_student(id:int) -> JSONResponse:
    for i in range(len(ListOfStudent)):
        print(ListOfStudent[i].id)
        if ListOfStudent[i].id == id:
            ListOfStudent.pop(i)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "data":"student was deleted"
                }
            )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='enternal error'
    )

@app.put("/putstudent/{id}")
def put_student(student:PutStudent, id) -> JSONResponse:
    for i in range(len(ListOfStudent)):
        if ListOfStudent[i].id == int(id):
            ListOfStudent.pop(i)
            break
    new_student = PutStudent(id=id, name=student.name, major=student.major, gender=student.gender )
    ListOfStudent.append(new_student)
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data":new_student
            }
        )


@app.patch("/patchstudent/{id}")
def patch_student(student:PatchStudent, id) -> JSONResponse:
    for i in range(len(ListOfStudent)):
        if ListOfStudent[i].id ==int(id):
            if student.name !=None:
                ListOfStudent[i].name=student.name
            if student.gender !=None:
                ListOfStudent[i].gender=student.gender
            if student.major != None:
                ListOfStudent[i].major=student.major
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "data":ListOfStudent[i]
                }
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )
