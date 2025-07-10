from fastapi import APIRouter, Body, Depends, Query, Request

from config import user_service
from utils.get_current_user import JWTBearer

user_router = APIRouter()


@user_router.post("/login")
async def login(username: str = Body(...), password: str = Body(...)):
    """
    User login endpoint

    Authenticates a user based on provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: A dictionary containing the user's authentication token.
    """
    return user_service.login(username, password)


@user_router.post("/register")
async def register(username: str = Body(...), password: str = Body(...)):
    """
    User registration endpoint

    Registers a new user with the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: A dictionary containing the success message.
    """
    return user_service.register(username, password)


@user_router.post("/logout", dependencies=[Depends(JWTBearer(user_service))])
async def logout(request: Request):
    """
    User logout endpoint

    Logs out the authenticated user.

    Args:
        request (Request): The HTTP request object.

    Returns:
        dict: A dictionary containing the success message.
    """
    token = request.headers["authorization"]
    return user_service.logout(token)


@user_router.get("/user", dependencies=[Depends(JWTBearer(user_service))])
async def get_user_details(username: str = Query(default=None)):
    """
    User get endpoint

    Retrieve details of the specified user.

    Args:
        username (str, optional): The username of the user to retrieve details for.

    Returns:
        dict: A dictionary containing the user details.
    """
    return user_service.get_user_details(username)


@user_router.post("/user", dependencies=[Depends(JWTBearer(user_service))])
async def set_user_details(username: str = Body(...), password: str = Body(...)):
    """
    User create/update endpoint

    Creates or updates details of the specified user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: A dictionary containing the success message.
    """
    return user_service.set_user_details(username, password)
