from fastapi import FastAPI
import uvicorn
import argparse
from db import DBDriver

app = FastAPI(debug=True)
from pydantic import BaseModel

class Review(BaseModel):
    tg_id: int
    tg_name: str
    file_id: str
    comments: str


@app.post("/add_review")
def add_review(request: Review):
    driver = DBDriver()
    driver.add_review(request)
    return {"status": "ok"}


if __name__ == "__main__":
    # setup_logging
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    args = vars(parser.parse_args())

    uvicorn.run(app, **args)
