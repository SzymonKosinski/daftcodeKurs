from fastapi import FastAPI, HTTPException, Response
import hashlib
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
def authorization(password : str, password_hash : str, response : Response):
    encrypted_password=hashlib.sha512(password.encode('utf-8')).hexdigest()
    if encrypted_password!=password_hash:
        raise HTTPException(status_code=401, detail="unathorized password")
    return {"item": "lol"}



#uvicorn main:app
