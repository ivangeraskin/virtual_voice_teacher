from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/add_user")
def add_user(request):
    return {"status": "ok"}

@app.get("/get_city")
def get_review(request):
    return {"status": "ok"}

if __name__ == "__main__":
    # setup_logging
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
