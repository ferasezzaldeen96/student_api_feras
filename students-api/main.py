import uuid

from sqlalchemy.sql.expression import select
from fastapi import FastAPI, status, HTTPException
from typing import Optional
from uuid import uuid4
from uuid import UUID
from models import PatchStudent, PostStudent, PutStudent, StudentResponse, TestDB, PostDB, PatchDB, PutDB
from session import JSONResponse
from db import engine
from db import students as student_table
from datetime import datetime


app= FastAPI()



@app.get("/getstudentbyid/{id}")
def  get_student_by_id(id:UUID) -> JSONResponse:
    with engine.connect() as conn:
        student = conn.execute(student_table.select().where(
            student_table.c.id == id)).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {id} dose not exist'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': TestDB(**student._asdict())}
    )


@app.post("/addstudent")
def add_new_student(student: PostDB) ->  JSONResponse:
    with engine.begin() as conn:
        new_student = conn.execute(student_table.insert().returning(student_table).values(**student.dict(exclude_none=True)))
        if not new_student:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='AN ERROR CAME UP '
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'data': new_student.first()}
        )


@app.get("/students")
def get_student(gender : Optional[str] = None, department : Optional[str] = None) -> JSONResponse:
    if not gender and not department:
        with engine.connect() as conn:
            students = conn.execute(select(student_table)).fetchall()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=(TestDB(**student._asdict()) for student in students)
        )
    if  gender and not department:
        with engine.connect() as conn:
            students = conn.execute(student_table.select().where(student_table.c.gender==gender)).fetchall()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=(TestDB(**student._asdict()) for student in students)
        )
    if  not gender and department:
        with engine.connect() as conn:
            students = conn.execute(student_table.select().where(student_table.c.department==department)).fetchall()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=(TestDB(**student._asdict()) for student in students)
        )
    if  gender and department:
        with engine.connect() as conn:
            students = conn.execute(student_table.select().where(student_table.c.department==department, student_table.c.gender==gender)).fetchall()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=(TestDB(**student._asdict()) for student in students)
        )





@app.delete("/deletestudent")
def delete_student(id:UUID) -> JSONResponse:
    with engine.begin() as conn:
        delete_student = conn.execute(student_table.delete().returning(student_table).where(student_table.c.id == id))
        deleted=delete_student.first()
        if  not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Student with id: {id} dose not exist'
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': deleted}
            )


@app.put("/putstudent/{id}")
def put_student(student:PutDB, id) -> JSONResponse:
    try :
        with engine.begin() as conn:
            updated_student = conn.execute(student_table.update().returning(student_table).where(student_table.c.id == id).values(**student.dict(exclude_none=True),updated_at= datetime.now()))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': updated_student.first()}
            )   
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='AN ERROR CAME UP '
        )


@app.patch("/patchstudent/{id}")
def patch_student(student:PatchDB, id) -> JSONResponse:
    try :
        with engine.begin() as conn:
            updated_student = conn.execute(student_table.update().returning(student_table).where(student_table.c.id == id).values(**student.dict(exclude_none=True),updated_at= datetime.now()))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': updated_student.first()}
            )        
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='AN ERROR CAME UP '
        )
