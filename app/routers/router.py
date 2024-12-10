from fastapi import APIRouter, Request, HTTPException, Response, status
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.responses import RedirectResponse
from starlette.config import Config
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

from app.resources.userprofile_resource import UserProfileResource
from app.utils import utils

auth_router = APIRouter()

config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 60

@auth_router.post("/user/{username}/register", tags=["user"])
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
        # return {"message": f"User '{username}' registered with ID {user_id}"}
        return Response(
            content=f"User '{username}' registered with ID {user_id}",
            status_code=status.HTTP_201_CREATED,
            headers={"Location": f"/user/{username}"}
        )
    else:
        raise HTTPException(status_code=500, detail="Registration failed")

def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=JWT_EXPIRES_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

@auth_router.get("/login/google", tags=["auth"])
async def login_via_google(request: Request):
    """
    Initiates Google OAuth login by redirecting the user to the Google authentication page.
    """
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get("/auth/google/callback", tags=["auth"])
async def auth_google_callback(request: Request):
    """
    Handles the callback after Google OAuth login.
    Redirects to the frontend upon successful authentication.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=400, detail="OAuth authentication failed")

    user_info = token.get('userinfo')
    print(user_info)
    if not user_info or 'email' not in user_info:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info from Google.")

    username = user_info['email']
    user_profile_resource = UserProfileResource(config={})

    # Check if the user already exists
    existing_user = user_profile_resource.get_by_key(username)
    if existing_user:
        user_id = existing_user.id
    else:
        # Register the user
        user_id = user_profile_resource.register_user(username)
        if not user_id:
            raise HTTPException(status_code=500, detail="Registration failed")

    # Notify about user login
    user_profile_resource.notify_user_login(username)

    # Create JWT token
    token_data = {"sub": username, "user_id": user_id}
    jwt_token = create_access_token(token_data)

    # Redirect to the frontend with the JWT token and username
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    redirect_url = f"{frontend_url}/auth/callback?token={jwt_token}&username={username}"
    return RedirectResponse(url=redirect_url)

@auth_router.get("/user/{username}", tags=["auth"], name="get_user_profile")
async def get_user_profile(username: str, request: Request):
    """
    Fetches the user's profile and includes HATEOAS links.
    """
    user_profile_resource = UserProfileResource(config={})
    user = user_profile_resource.get_by_key(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_profile_resource.notify_user_login(username)
    
    # Generate HATEOAS links
    links = utils.generate_user_links(request, username)

    return {
        "user": user,
        "username": username,
        "_links": links
    }
