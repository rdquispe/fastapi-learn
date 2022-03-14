# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastApi
from fastapi import FastAPI, Body, Query

app = FastAPI()


# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"Hello": "Rodrigo"}


# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(default=None, min_length=1, max_length=50),
    age: Optional[str] = Query(...)
):
    return {name: age}
