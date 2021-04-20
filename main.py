from fastapi import FastAPI
app = FastAPI()




@app.get('/method')
def root():
    return {"method": "GET"}



root()
#uvicorn main:app
