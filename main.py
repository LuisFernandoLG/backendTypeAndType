from typing import Optional

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def get_basic_information():
    return {"Hello": "World"}
