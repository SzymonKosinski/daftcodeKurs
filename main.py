import json

import aiosqlite
from fastapi import FastAPI, HTTPException, Response, status, Cookie
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
from fastapi.responses import PlainTextResponse, JSONResponse,RedirectResponse
from datetime import date, timedelta
from pydantic import BaseModel
import random
import string
import sqlite3




app = FastAPI()
conn = sqlite3.connect("northwind.db")
app.access_tokens = []
app.access_logins = []

def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(29))
    return result_str


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
        if len(app.access_logins)==3:
            app.access_logins.pop(0)
        login=get_random_string()
        app.access_logins.append(login)
        response.set_cookie(key="session_token", value=login)
        return response
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED




@app.post("/login_token", status_code=201)
def weryfikacja(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username=="4dm1n" and credentials.password=="NotSoSecurePa$$":
        response.status_code = status.HTTP_201_CREATED
        if len(app.access_tokens)==3:
            app.access_tokens.pop(0)
        token_value = get_random_string()
        app.access_tokens.append(token_value)
        return {"token": token_value}
    else:
        raise HTTPException(status_code=401, detail="unathorized password")

@app.get("/welcome_session")
def welcome_session(*, response: Response, session_token: str = Cookie(None), format: str = ""):
    if session_token not in app.access_logins:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    else:
        response.status_code = status.HTTP_200_OK
        if format == "":
            result = "Welcome!"
            return PlainTextResponse(content=result, status_code=200)
        elif format == "json":
            result = {"message": "Welcome!"}
            return JSONResponse(content=result, status_code=200)
        elif format == "html":
            html = f"""
                    <html>
                        <body>
                            <h1>Welcome!</h1>
                        </body>
                    </html>
                    """
            return HTMLResponse(content=html, status_code=200)
        else:
            result = "Welcome!"
            return PlainTextResponse(content=result, status_code=200)



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
@app.delete("/logout_session")
def logout_session(*, response: Response, session_token: str = Cookie(None), format: str = ""):
    if session_token not in app.access_logins:
        response.status_code = status.HTTP_401_UNAUTHORIZED

    else:
        for token_number in range(len(app.access_tokens)):
            if app.access_logins[token_number]==session_token:
                app.access_logins.pop(token_number)
                break
        response.status_code = status.HTTP_302_FOUND
        return RedirectResponse(f"https://daftcodeplikacja.herokuapp.com/logged_out?token={session_token}&format={format}"
                                , status_code=303)
@app.delete("/logout_token")
def logout_session(response : Response, token: str = "", format: str = ""):
    if token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="unathorized session")
    else:
        for token_number in range(len(app.access_tokens)):
            if app.access_tokens[token_number]==token:
                app.access_tokens.pop(token_number)
                break
        response.status_code = status.HTTP_302_FOUND
        return RedirectResponse(f"https://daftcodeplikacja.herokuapp.com/logged_out?token={token}&format={format}"
                                ,status_code=303)

@app.get("/logged_out")
def logged_out(response: Response, format: str=""):
    if format == "":
        result = "Logged out!"
        return PlainTextResponse(content=result, status_code=200)
    elif format == "json":
        result = {"message": "Logged out!"}
        return JSONResponse(content=result, status_code=200)
    elif format == "html":
        html = f"""
                <html>
                    <body>
                        <h1>Logged out!</h1>
                    </body>
                </html>
                """
        return HTMLResponse(content=html, status_code=200)
    else:
        result = "Logged out!"
        return PlainTextResponse(content=result, status_code=200)

@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    await app.db_connection.close()
@app.get("/categories")
async def categories(response: Response):
    cursor = await app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID")
    data = await cursor.fetchall()

async def categories(response: Response):
    cursor = await app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID")
    data = await cursor.fetchall()
    print(data)
    return {
        "categories": [
            {"id": int(x[0]), "name": f"{x[1]}"} for x in data
        ]
    }
@app.get("/customers")
async def customers(response: Response):
    cursor = await app.db_connection.execute("SELECT CustomerID, CompanyName, (COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, ''))  FROM Customers ORDER BY UPPER(CustomerID)")
    data = await cursor.fetchall()
    return  {
        "customers": [
            {"id": f"{x[0]}", "name": f"{x[1]}", "full_adress": f"{x[2]}"} for x in data
            ]
    }
# uvicorn main:app
