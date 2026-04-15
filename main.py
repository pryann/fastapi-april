from random import randint
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status

from schemas import Item, ItemCreate, ItemPartialUpdate, ItemQuery
from utils import generate_id

app = FastAPI()

items: list[Item] = [
    Item(id=i, name=f"Item-{i}", quantity=randint(0, 20), company_id=randint(1, 5)) for i in range(1, 51)
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items", response_model=list[Item])
def get_items(query: Annotated[ItemQuery, Query()]):
    sorted_items = sorted(items, key=lambda item: getattr(item, query.order_by))
    return sorted_items[query.offset : query.offset + query.limit]


@app.get("/items/{item_id}", response_model=Item)
def find_item_by_id(item_id: int):
    # refactor this code to use a separeted function to find the item by id, to avoid code duplication
    for existing_item in items:
        if existing_item.id == item_id:
            return existing_item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=Item)
def create_item(item: ItemCreate):
    # ids = [existing_item.id for existing_item in items]
    # actual_max = max(ids) if ids else 0
    # new_id = actual_max + 1
    # use a separeted function to generate the new id, to avoid code duplication
    new_id = generate_id(items)
    new_item = Item(id=new_id, **item.model_dump())
    items.append(new_item)
    # it can be problematic, if the dataset not updated
    # return new_item
    # but if we want to be sure that the dataset is updated, we can return the last item in the list
    return items[-1]


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            items[index] = item
            return items[index]
    # raise HTTPException(status_code=404, detail="Item not found")
    items.append(item)
    return items[-1]


@app.patch("/items/{item_id}", response_model=Item)
def partial_update(item_id: int, item: ItemPartialUpdate):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            # use exclude_unset=True to only update the fields that are provided in the request
            items[index] = existing_item.model_copy(update=item.model_dump(exclude_unset=True))
            return items[index]
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            del items[index]
            return
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/companies/{company_id}/items", response_model=list[Item])
def get_company_items(company_id: int, query: Annotated[ItemQuery, Query()]):
    company_items = [item for item in items if item.company_id == company_id]
    sorted_items = sorted(company_items, key=lambda item: getattr(item, query.order_by))
    return sorted_items[query.offset : query.offset + query.limit]


@app.get("/companies/{company_id}/items/{item_id}", response_model=Item)
def find_company_item(company_id: int, item_id: int):
    item = [
        exsisted_item
        for exsisted_item in items
        if exsisted_item.company_id == company_id and exsisted_item.id == item_id
    ]
    if len(item) > 0:
        return item[0]
    raise HTTPException(status_code=404, detail="Company item not found")


if __name__ == "__main__":
    print("Starting FastAPI application...")
