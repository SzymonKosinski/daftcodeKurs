from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
def root():
    print("teeest")
    print("test 2")
    return {"message": "Hello World"}

root()
