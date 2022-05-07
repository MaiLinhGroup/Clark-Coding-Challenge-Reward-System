from fileinput import filename
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/scoring")
async def calculate_score(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "contents": contents.split(b'\n')}