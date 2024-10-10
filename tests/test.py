from fastapi import FastAPI, Query
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    item_id: int
    name: str = "sanju"
    price: float = None

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/")
def read_item(
    item_id: int = Query(..., description="The ID of the item"),
    name: str = Query("sanju", max_length=50, description="The name of the item"),
    price: float = Query(None, gt=0, description="The price of the item")
):
    item = Item(item_id=item_id, name=name, price=price)
    return item

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=1234)
