from datetime import datetime

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from utils.logger import logger


class JWTBearer(HTTPBearer):
    """
    JWT Bearer token authentication middleware.

    Extends HTTPBearer for JWT (JSON Web Token) authentication.
    Verifies the validity of JWT tokens and their association with user sessions.

    Args:
        user_service: An instance of the UserService class for token verification.
        auto_error (bool, optional): Whether to raise HTTPException automatically on authentication error.
                                     Defaults to True.
    """

    def __init__(self, user_service, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.user_service = user_service

    async def __call__(self, request: Request):
        """
        Middleware to validate JWT tokens.

        Verifies the JWT token provided in the request header.
        Raises HTTPException if the token is invalid or expired.

        Args:
            request (Request): The HTTP request object.

        Returns:
            str: The JWT token if valid.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        """
        Verify JWT token validity.

        Verifies the validity of the provided JWT token.
        Updates user session if the token is valid.

        Args:
            jwt_token (str): The JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        isTokenValid: bool = True
        try:
            #payload = self.user_service.decodeJWT(jwt_token)
            if jwt_token in self.user_service.sessions:
                self.user_service.sessions[jwt_token] = datetime.utcnow()
            else:
                isTokenValid = False
        except Exception as e:
            logger.info("error: ", str(e))
            isTokenValid = False

        return isTokenValid
