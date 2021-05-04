import json

from fastapi import FastAPI, HTTPException, Response, status, Cookie
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import date, timedelta
from pydantic import BaseModel

app = FastAPI()
app.access_tokens = []
app.access_logins = []


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

@app.get("/method", response_class=PlainTextResponse)
def method():
    app.method = "GET"
    return {"test" : "test"}


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
@app.post("/login_session")
def logowanie(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username=="4dm1n" and credentials.password=="NotSoSecurePa$$":
        response.status_code = status.HTTP_201_CREATED
        response.set_cookie(key="session_token", value="stary winiary")
        app.access_logins.append("stary winiary")
        return response
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED




@app.post("/login_token", status_code=201)
def weryfikacja(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username=="4dm1n" and credentials.password=="NotSoSecurePa$$":
        response.status_code = status.HTTP_201_CREATED
        token_value = "dwa"
        global token_login_token
        token_login_token = token_value
        app.access_tokens.append(token_value)
        return {"token": token_value}
    else:
        raise HTTPException(status_code=401, detail="unathorized password")

@app.get("/welcome_session")
def welcome_session(*, response : Response, token: str = Cookie(None), format: str = ""):
    if token not in app.access_logins:
        raise HTTPException(status_code=401, detail="unathorized session")
    elif format == "":
        result = "Welcome!"
        return PlainTextResponse(content=result)
    elif format == "json":
        result = {"message": "Welcome!"}
        return JSONResponse(content=result)
    elif format == "html":
        result = ''' 
       <html>
           <h1>Welcome!</h1>
       </html>'''
        return HTMLResponse(content=result)
    else:
        result = "Welcome!"
        return PlainTextResponse(content=result)



@app.get("/welcome_token")
def welcome_token(response : Response, token: str = "", format: str = ""):
    if token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="unathorized session")
    elif format == "":
        result = "Welcome!"
        return PlainTextResponse(content=result)
    elif format == "json":
        result = {"message": "Welcome!"}
        return JSONResponse(content=result)
    elif format == "html":
        result= ''' 
        <html>
            <h1>Welcome!</h1>
        </html>'''
        return HTMLResponse(content=result)
    else:
        result = "Welcome!"
        return PlainTextResponse(content=result)

# uvicorn main:app
