from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from sqlalchemy import text
from sqlmodel import Session

from database.database import engine


def get_students_list():
    with Session(engine) as session:
        query = f"""
            select id, name from users
            where is_admin is not true
            and is_active is true;
            """

        result = session.execute(text(
            query
        )).all()

    return [{
        "id": r[0],
        "name": r[1],
    } for r in result]
