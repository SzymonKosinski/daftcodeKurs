from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
def root():
    print("teeest123")
    return {"message": "Hello World"}

root()
