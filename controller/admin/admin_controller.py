from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine
from service.admin.admin_service import get_students_list
from service.auth.auth_service import login

admin = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@admin.get("/students")
async def get_students():
    return get_students_list()
