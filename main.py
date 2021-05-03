from fastapi import FastAPI, HTTPException, Response, status, Request, Depends, security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
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

security = HTTPBasic()
@app.post("/login_session", status_code=201)
def logowanie(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username=="4dm1n" and credentials.password=="NotSoSecurePa$$":
        response.set_cookie(key="session_token", value="stary winiary")
        global token_login_session
        token_login_session = "stary winiary"
        return response
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED




@app.post("/login_token", status_code=201 )
def weryfikacja(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username=="4dm1n" and credentials.password=="NotSoSecurePa$$":
        token_value = "dwa"
        return "token:"f"{token_value}"
    else:
        raise HTTPException(status_code=401, detail="unathorized password")


# uvicorn main:app
