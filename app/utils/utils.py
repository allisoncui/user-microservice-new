from pydantic import BaseModel
from fastapi import Request
from typing import Dict

class Link(BaseModel):
    href: str
    method: str

def generate_user_links(request: Request, username: str) -> Dict[str, Link]:
    # Full path to the specific user profile resource
    self_url = str(request.url_for("get_user_profile", username=username))
    base_url = str(request.base_url).rstrip("/")

    return {
        "self": Link(href=self_url, method="GET"),
        "add": Link(href=self_url, method="POST"),
        "viewed_restaurants": Link(
            href=f"{base_url}/user/{username}/viewed_restaurants", method="GET"
        ),
    }
