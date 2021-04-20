from fastapi import FastAPI
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

@app.get("/auth")
def authorization(password, password_hash):
    encrypted_password=hashlib.sha256(password.encode('utf-8')).hexdigest()
    if(encrypted_password==password_hash):
        return 204
    else:
        return 401


#uvicorn main:app
