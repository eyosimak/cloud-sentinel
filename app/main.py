from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to cloud sentinel!"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "Version": "0.1.0"}
