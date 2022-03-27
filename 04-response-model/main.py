# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastApi
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models

class HairColor(Enum):
    white = 'white'
    black = 'black'
    brown = 'brown'
    blonde = 'blonde'
    red = 'red'


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=100)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Rodrigo",
                "last_name": "Quispe",
                "age": 30,
                "hair_color": "black",
                "is_married": False,
                "password": "soyunpassword"
            }
        }


class Location(BaseModel):
    city: str = Field(example="La Paz")
    state: str = Field(example="La Paz")
    country: str = Field(example="Bolivia")

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "city": "La Paz",
    #             "state": "La Paz",
    #             "country": "Bolivia"
    #         }
    #     }


@app.get("/")
def home():
    return {"Hello": "Rodrigo"}


# Request and Response Body

@app.post("/person/new", response_model=Person, response_model_exclude={'password'})
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50, example="Rocío"),
    age: str = Query(..., example=25)
):
    return {name: age}


# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(..., gt=0, example=1)):
    return {person_id: "exist"}


# Validaciones: Request Body

@app.put("/person/detail/{person_id}")
def update_person(
    person_id: int = Path(..., gt=0, example=123),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
