from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from consts import DB_PASSWORD,DB_HOST,DB_INIT_DATABASE,DB_PORT,DB_TYPE

app = FastAPI()

# Schema for your dictionary
class PersonalData(BaseModel):
    first_name: str
    family_name: str
    gender: str
    hobbies: str

@app.post("/print_data/")
async def print_data(data: PersonalData):
    # Convert to dictionary and print
    dict_data = data.model_dump()
    print("Received personal data:", dict_data)
    return {"message": "Data received and printed", "data": dict_data}
