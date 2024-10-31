from pydantic import BaseModel
from typing import Optional, List

class Link(BaseModel):
    href: str
    method: str

class UserProfile(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    viewed_restaurants: Optional[str] = None  # Stores restaurant codes as comma-separated values

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "allison_cuii",
                "viewed_restaurants": "69593,65452,64593"
            }
        }

class ViewedRestaurantsResponse(BaseModel):
    viewed_restaurants: List[str]
    links: dict[str, Link]
