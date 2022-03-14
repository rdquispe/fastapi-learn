# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastApi
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


class Location(BaseModel):
    city: str
    state: str
    country: str


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
    age: Optional[str] = Query(..., title="Person Age")
):
    return {name: age}


# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(..., gt=0)):
    return {person_id: "exist"}


# Validaciones: Request Body

@app.put("/person/detail/{person_id}")
def update_person(
    person_id: int = Path(..., gt=0),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
