from fastapi import FastAPI, HTTPException, Response, status, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
import hashlib
import base64
import http.cookies
from datetime import date, timedelta
from pip._vendor.requests.auth import HTTPBasicAuth
from pydantic import BaseModel

app = FastAPI()

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
       </html>'''.format(aktualnaData=date.today())


@app.post("/login_session", status_code=201)
def logowanie(login: str="", haslo:str = ""):
    auth=HTTPBasicAuth(login, haslo)
    response = Response()
    if auth.username=="4dm1n" and auth.password=="NotSoSecurePa$$":
        response.set_cookie(key="session_token", value="stary winiary")
        global token_login_session
        token_login_session = "stary winiary"
        return response
    else:
        raise HTTPException(status_code=401, detail="unathorized password")




@app.post("/login_token", status_code=201 )
def weryfikacja(login: str=""):
    b = bytes(login, 'utf-8')
    loginBase64 = base64.b64encode(b)
    klucz = "4dm1n:NotSoSecurePa$$"
    b = bytes(klucz, 'utf-8')
    kluczBase64 = base64.b64encode(b)
    kluczBase64 = kluczBase64.decode('utf-8')
    loginBase64 = loginBase64.decode('utf-8')
    #print(kluczBase64)
    if kluczBase64 == loginBase64 or login==kluczBase64:
        token = klucz
        return "token:"f"{token}"
    else:
        raise HTTPException(status_code=401, detail="unathorized password")


logowanie( "4dm1n", "NotSoSecurePa$$")
weryfikacja("NGRtMW46Tm90U29TZWN1cmVQYSQk")
# uvicorn main:app
