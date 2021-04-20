from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()




@app.get('/method')
def root():
    return {"method": "GET"}



root()
#uvicorn main:app
