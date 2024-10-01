from fastapi import APIRouter, HTTPException
from app.resources.userprofile_resource import UserProfileResource

router = APIRouter()

# Get user profile by username
@router.get("/api/user/{username}", tags=["user"])
async def get_user_profile(username: str):
    # Initialize the UserProfileResource
    user_profile_resource = UserProfileResource(config={})

    # Retrieve user profile using the get_by_key method
    result = user_profile_resource.get_by_key(username)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Get viewed restaurants by username
@router.get("/api/user/{username}/viewed_restaurants", tags=["user"])
async def get_viewed_restaurants(username: str):
    # Initialize the UserProfileResource
    user_profile_resource = UserProfileResource(config={})

    # Retrieve the viewed restaurants using the get_viewed_restaurants method
    viewed_restaurants = user_profile_resource.get_viewed_restaurants(username)
    if viewed_restaurants:
        return {"username": username, "viewed_restaurants": viewed_restaurants}
    else:
        raise HTTPException(status_code=404, detail="No viewed restaurants found for this user")
