from typing import List, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

fake_items_db = [{"item_name": "foo"}, {"item_name:": "blalba"}, {"item_name": "adsfaf"}]


class Item(BaseModel):
    name: str
    description: Optional[str] = None  # it's optional -> if it is not in request body, it's ok
    price: float
    tax: Optional[float] = None


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/users/{user_id}/items/{item_id}")  # {}안에 없는 거는 query string
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


# request body
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"pricet_with_tax": price_with_tax})
    return item_dict


# request body + path parameter
@app.put("/items/{item_id}")
async def put_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# request body + path parameter + query string
@app.put("/items/{item_id}/{item_special}")
async def put_item_2(item_id: int, item_special: str, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# import Query - validations
@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None,
                                              max_length=50, min_length=3,
                                              regex="^fixedquery$")):  # q: Optional[str] = Query(None) is same as q: Optional[str] = None
    results = {"items": "blahblah"}
    if q:
        results.update({"q": q})
    return results
