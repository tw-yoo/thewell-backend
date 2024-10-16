from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from sqlalchemy import text
from sqlmodel import Session

from database.database import engine


def get_students_list():
    with Session(engine) as session:
        query = f"""
            select id, name, is_active from users
            where is_admin is not true;
            """

        result = session.execute(text(
            query
        )).all()
        print(result)

    return "OK"
