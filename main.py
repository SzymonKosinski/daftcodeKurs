from fastapi import FastAPI, HTTPException, Response, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
import hashlib
import base64
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
def authorization(password="", password_hash="", response=Response):
    encrypted_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    if encrypted_password != password_hash:
        raise HTTPException(status_code=401, detail="unathorized password")
    elif password == "":
        raise HTTPException(status_code=401, detail="unathorized password")
    return {"item": "lol"}


def number_of_letters(word):
    result = 0
    for character in word:
        if character.isalpha():
            result += 1
    return result


class Register(BaseModel):
    name: str
    surname: str


app.id_counter = 0
app.registration = dict()


@app.post("/register")
def register(response: Response, register_person: Register):
    register_date = date.today()
    days_to_add = number_of_letters(register_person.name) + number_of_letters(register_person.surname)
    vaccination_date = register_date + timedelta(days_to_add)

    app.id_counter += 1

    response.status_code = status.HTTP_201_CREATED
    data_of_person_to_be_registered = dict()
    data_of_person_to_be_registered["id"] = app.id_counter
    data_of_person_to_be_registered["name"] = register_person.name
    data_of_person_to_be_registered["surname"] = register_person.surname
    data_of_person_to_be_registered["register_date"] = register_date
    data_of_person_to_be_registered["vaccination_date"] = vaccination_date
    app.registration[app.id_counter] = data_of_person_to_be_registered

    return data_of_person_to_be_registered


@app.get("/patient/{id}")
def patient(response: Response, id: int):
    if id > app.id_counter:  # nie ma takiego pacjenta
        response.status_code = status.HTTP_404_NOT_FOUND
        return response.status_code
    elif id < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response.status_code

    return app.registration[id]


@app.get("/hello", response_class=HTMLResponse)
def message():
    return '''
       <html>
           <head>
               <title>Some HTML in here</title>
           </head>
           <body>
               <h1>Hello! Today date is {aktualnaData}</h1>
           </body>
       </html>
       '''.format(aktualnaData=date.today())


@app.post("/login_session")
def logowanie(login: str):
    b=bytes(login, 'utf-8')
    loginBase64 = base64.b64encode(b)
    klucz="4dm1n:NotSoSecurePa$$"
    b=bytes(klucz, 'utf-8')
    kluczBase64=base64.b64encode(b)
    if kluczBase64!=loginBase64:
        raise HTTPException(status_code=401, detail="unathorized password")
    else:
        response = JSONResponse(content=loginBase64)
        response.set_cookie(key="fakesession", value="fake-cookie-session-value")



@app.post("/login_token")
def weryfikacja(login=""):
    b = bytes(login, 'utf-8')
    loginBase64 = base64.b64encode(b)
    klucz = "4dm1n:NotSoSecurePa$$"
    b = bytes(klucz, 'utf-8')
    kluczBase64 = base64.b64encode(b)
    if kluczBase64 != loginBase64:
        raise HTTPException(status_code=401, detail="unathorized password")
    else:
        return "{token:{}}".format(login)


# uvicorn main:app
