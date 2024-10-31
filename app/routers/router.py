from app.resources.userprofile_resource import UserProfileResource
from fastapi import APIRouter, HTTPException, Response, status, Request
from app.utils import utils

router = APIRouter()

@router.post("/user/{username}/register", tags=["user"])
async def register_user(username: str):
    user_profile_resource = UserProfileResource(config={})
    
    existing_user = user_profile_resource.get_by_key(username)
    if existing_user:
        return Response(
            content=f"User '{username}' already exists",
            status_code=status.HTTP_200_OK
        )

    user_id = user_profile_resource.register_user(username)
    if user_id:
        #return {"message": f"User '{username}' registered with ID {user_id}"}
        return Response(
            content=f"User '{username}' registered with ID {user_id}",
            status_code=status.HTTP_201_CREATED,
            headers={"Location": f"/user/{username}"}
        )
    else:
        raise HTTPException(status_code=500, detail="Registration failed")

@router.get("/user/{username}", tags=["user"], name="get_user_profile")
async def get_user_profile(username: str, request: Request):
    user_profile_resource = UserProfileResource(config={})
    user = user_profile_resource.get_by_key(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate HATEOAS links
    links = utils.generate_user_links(request, username)

    return {
        "user": user,
        "username": username,
        "_links": links
    }