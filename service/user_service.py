import time
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException


class UserService:
    def __init__(self):
        """
        Initializes the UserService.

        Initializes user database, session storage, expiration time for tokens,
        secret key for token generation, and algorithm for token encoding.
        """
        self.users_db = {}
        self.sessions = {}
        self.expiry_time = 15
        self.secret_key = "secret"
        self.algo = 'HS256'

    def login(self, username: str, password: str):
        """
        User login.

        Authenticates a user based on provided username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary containing the success message and authentication token.

        Raises:
            HTTPException: If the username or password is invalid.
        """
        if username in self.users_db and self.users_db[username] == password:
            token = self.create_token(username)
            self.sessions[token] = datetime.utcnow()
            return {"message": "Login successful", "token": token}
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")

    def register(self, username: str, password: str):
        """
        User registration.

        Registers a new user with the provided username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary containing the success message.

        Raises:
            HTTPException: If the username already exists.
        """
        if username in self.users_db:
            raise HTTPException(status_code=400, detail="Username already exists")
        self.users_db[username] = password
        return {"message": "Registration successful"}

    def logout(self, token: str):
        """
        User logout.

        Logs out the authenticated user.

        Args:
            token (str): The authentication token.

        Returns:
            dict: A dictionary containing the success message.
        """
        if token in self.sessions:
            del self.sessions[token]
        return {"message": "Logout successful"}

    def get_user_details(self, username: str):
        """
        Get user details.

        Retrieve details of the specified user.

        Args:
            username (str): The username of the user to retrieve details for.

        Returns:
            dict: A dictionary containing the user details.

        Raises:
            HTTPException: If the user is not found.
        """
        if username in self.users_db:
            return {"username": username, "password": self.users_db[username]}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    def set_user_details(self, username: str, password: str):
        """
        Set user details.

        Creates or updates details of the specified user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary containing the success message.
        """
        self.users_db[username] = password
        return {"message": "User details updated"}

    def create_token(self, username: str, expires_delta: Optional[timedelta] = None):
        """
        Create authentication token.

        Creates a JWT authentication token for the specified user.

        Args:
            username (str): The username of the user.
            expires_delta (timedelta, optional): Expiration time delta for the token.

        Returns:
            str: The generated authentication token.
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.expiry_time)
        token = jwt.encode({"sub": username, "exp": expire}, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token: str):
        """
        Verify authentication token.

        Verifies the validity of the provided authentication token.

        Args:
            token (str): The authentication token.

        Returns:
            str: The username associated with the token.

        Raises:
            HTTPException: If the token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithm='HS256')
            username = payload["sub"]
            if token in self.sessions:
                self.sessions[token] = datetime.utcnow()
            return username
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")

