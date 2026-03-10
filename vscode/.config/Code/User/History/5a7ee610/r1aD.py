from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from crud import create_info
from consts import DB_PASSWORD,DB_HOST,DB_INIT_DATABASE,DB_PORT,DB_TYPE

app = FastAPI()


class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    gender: str
    hobbies: str

@app.post("/print_data/")
async def print_data(data: PersonalInfo):

    create_info(data.first_name)

    

    return {"message": "Data received and printed", "data": data}
