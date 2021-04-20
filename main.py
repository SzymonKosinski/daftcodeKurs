from fastapi import FastAPI
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


#uvicorn main:app
