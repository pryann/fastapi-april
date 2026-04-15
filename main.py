from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    quantity: int


class ItemCreate(BaseModel):
    name: str
    quantity: int


class ItemPartialUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None


items: list[Item] = [
    Item(id=1, name="Item1", quantity=10),
    Item(id=2, name="Item2", quantity=5),
    Item(id=3, name="Item3", quantity=2),
]


def generate_id():
    return max([existing_item.id for existing_item in items], default=0) + 1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items", response_model=list[Item])
def get_items():
    return items


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
    new_id = generate_id()
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


if __name__ == "__main__":
    print("Starting FastAPI application...")
