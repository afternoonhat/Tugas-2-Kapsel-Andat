from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from datetime import datetime
from enum import Enum
import re

class Item(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=100, pattern=r'^[a-zA-Z0-9 ]+$', title="Name of the item", example="IniAbadi33x")
    description: Optional[str] = None
    price: float = Field(gt=0, description="The price must be greater than zero", example=199.99)

    model_config = ConfigDict(extra="forbid")
