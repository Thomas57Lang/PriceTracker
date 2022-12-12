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

@app.get("/")
async def read_root():
    data = readdb.read_db("Item")
    return data

@app.get("/item/")
async def read_item(table_name: str = "ASIItem", sku: str = "206704"):
    data = readdb.read_item_db(table_name, sku)
    return data
