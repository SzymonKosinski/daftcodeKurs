from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
def root():
    print("teeest")
    return {"message": "Hello World"}

root()
