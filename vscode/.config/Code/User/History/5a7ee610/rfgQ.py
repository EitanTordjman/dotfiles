from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Schema for your dictionary
class PersonalData(BaseModel):
    first_name: Optional[str] = None
    family_name: Optional[str] = None
    gender: Optional[str] = None
    hobbies: Optional[Union[list[str], str]] = None

@app.post("/print_data/")
async def print_data(data: PersonalData):
    # Convert to dictionary and print
    dict_data = data.model_dump()
    print("Received personal data:", dict_data)
    return {"message": "Data received and printed", "data": dict_data}
