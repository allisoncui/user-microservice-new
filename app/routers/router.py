from fastapi import APIRouter, HTTPException
from app.resources.userprofile_resource import UserProfileResource

router = APIRouter()

@router.get("/user/{username}", tags=["user"])
async def get_user_profile(username: str):
    user_profile_resource = UserProfileResource(config={})

    result = user_profile_resource.get_by_key(username)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/user/{username}/register", tags=["user"])
async def register_user(username: str):
    user_profile_resource = UserProfileResource(config={})

    user_id = user_profile_resource.register_user(username)
    if user_id:
        return {"message": f"User '{username}' registered with ID {user_id}"}
    else:
        raise HTTPException(status_code=500, detail="Registration failed")

@router.get("/user/{username}/viewed_restaurants", tags=["user"])
async def get_viewed_restaurants(username: str):
    user_profile_resource = UserProfileResource(config={})

    viewed_restaurants = user_profile_resource.get_viewed_restaurants(username)
    if viewed_restaurants:
        return {"username": username, "viewed_restaurants": viewed_restaurants}
    else:
        raise HTTPException(status_code=404, detail="No viewed restaurants found for this user")
