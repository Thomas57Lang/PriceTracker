from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import readdb

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


data = readdb.read_db("ASIItem")


@app.get("/")
async def read_root():
    return data

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
