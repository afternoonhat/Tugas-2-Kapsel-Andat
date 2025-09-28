from fastapi import APIRouter, HTTPException
from modules.items.schema.schemas import Item
from modules.items.routes.createItem import items

router = APIRouter()

@router.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            items.pop(index)
            return {"message": f"Item {item_id} deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
