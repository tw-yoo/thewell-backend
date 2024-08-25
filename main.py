from fastapi import FastAPI

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def create_upload_file(image: UploadFile):
    return {"filename": image.filename}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
