from fastapi import FastAPI, HTTPException, Response
import hashlib
from datetime import date, timedelta
from pydantic import BaseModel



app = FastAPI()


@app.get("/method")
def method():
    app.method = "GET"
    return {"method": app.method}


@app.put('/method')
def root_put():
    return {"method": "PUT"}

@app.options('/method')
def root_Options():
    return {"method": "OPTIONS"}

@app.delete('/method')
def root_delete():
    return {"method": "DELETE"}

@app.post('/method', status_code=201)
def root_post():
    return {"method": "POST"}

@app.get("/auth", status_code=204)
def authorization(password ="", password_hash ="", response = Response):
    encrypted_password=hashlib.sha512(password.encode('utf-8')).hexdigest()
    if encrypted_password!=password_hash:
        raise HTTPException(status_code=401, detail="unathorized password")
    elif password=="":
        raise HTTPException(status_code=401, detail="unathorized password")
    return {"item": "lol"}

class Register(BaseModel):
    name: str
    surname: str


app.id_counter = 0
app.registration = dict()
@app.post("/register", status_code=201)
def register(response: Response, register_person: Register):
    register_date = date.today()
    days_to_add = len(register_person.name) + len(register_person.surname)
    vaccination_date = register_date + timedelta(days_to_add)

    app.id_counter += 1
    data_of_person_to_be_registered = dict()
    data_of_person_to_be_registered["id"] = app.id_counter
    data_of_person_to_be_registered["name"] = register_person.name
    data_of_person_to_be_registered["surname"] = register_person.surname
    data_of_person_to_be_registered["register_date"] = register_date
    data_of_person_to_be_registered["vaccination_date"] = vaccination_date
    app.registration[app.id_counter] = data_of_person_to_be_registered

    return data_of_person_to_be_registered


#uvicorn main:app
