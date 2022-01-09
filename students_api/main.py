
from typing import Optional
from uuid import UUID

from db import engine, students
from fastapi import FastAPI, HTTPException, status
from models import BaseStudent, PatchStudent, PostStudent, PutStudent
from session import JSONResponse

app = FastAPI()


@app.get('/students/{id}', response_model=BaseStudent)
def get_student_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        student = conn.execute(students.select().where(
            students.c.id == id)).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {id} dose not exist'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': BaseStudent(**student._asdict())}
    )


@app.post('/students', response_model=BaseStudent)
def add_new_student(student: PostStudent) -> JSONResponse:
    with engine.begin() as conn:
        new_student = conn.execute(students.insert().returning(
            students).values(**student.dict()))

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'data': BaseStudent(**new_student.first())}
        )


@app.get('/students', response_model=BaseStudent)
def get_student(gender: Optional[str] = None,
                department: Optional[str] = None) -> JSONResponse:
    sel = None
    if gender and department:
        sel = students.select().where(students.c.gender == gender)\
            .where(students.c.department == department)
    elif gender and not department:
        sel = students.select().where(students.c.gender == gender)
    elif department and not gender:
        sel = students.select().where(students.c.department == department)
    else:
        sel = students.select()

    with engine.connect() as conn:
        students_data = conn.execute(sel).fetchall()

    if not students_data:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'data': []}

        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': (BaseStudent(**student._asdict())
                 for student in students_data)}
    )


@app.delete('/students')
def delete_student(student_id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        deleted_student = conn.execute(students.delete().where(
            students.c.id == student_id
        )).rowcount

    if not deleted_student:
        raise HTTPException(
            status_code=404,
            detail=f'Student with id: ({student_id}) dose not exist'
        )
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                        content=f'Student with id: {student_id} deleted')


@app.put('/students/{id}', response_model=BaseStudent)
def put_student(student: PutStudent, student_id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        deleted_student = conn.execute(students.delete().where(
            students.c.id == student_id
        )).rowcount

        new_student = conn.execute(
            students.insert().values(id=student_id,
                                     **student.dict()).returning(students))

        if deleted_student:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={'data': BaseStudent(**new_student.first())})


@app.patch('/students/{id}', response_model=BaseStudent)
def patch_student(student: PatchStudent, id: UUID) -> JSONResponse:
    try:
        with engine.begin() as conn:
            updated_student = conn.execute(students.update().where(
                students.c.id == id)
                .values(**student.dict(exclude_none=True)).returning(students))

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': updated_student.first()}
            )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='AN ERROR CAME UP '
        )
