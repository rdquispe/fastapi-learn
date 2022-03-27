# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastApi
from fastapi import FastAPI, Body, Query, Path, status, Form

app = FastAPI()


# Models

class HairColor(Enum):
    white = 'white'
    black = 'black'
    brown = 'brown'
    blonde = 'blonde'
    red = 'red'


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=100)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


class Person(PersonBase):
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


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="rodrigo2022")
    message: str = Field(default="Login Successfully!")


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


@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "Rodrigo"}


# Request and Response Body

@app.post(path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters

@app.get(path="/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50, example="Rocío"),
    age: str = Query(..., example=25)
):
    return {name: age}


# Validaciones: Path Parameters

@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(person_id: int = Path(..., gt=0, example=1)):
    return {person_id: "exist"}


# Validaciones: Request Body

@app.put(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(..., gt=0, example=123),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results


# Form
@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)
