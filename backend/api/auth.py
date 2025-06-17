import logging
from fastapi import APIRouter, Depends, HTTPException, Header
import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

router = APIRouter()
logger = logging.getLogger(__name__)


class LoginRequest(BaseModel):
    """
    Pydantic model for login request.
    """
    password: str


class RefreshTokenRequest(BaseModel):
    """
    Pydantic model for refresh token request.
    """
    refresh_token: str


def authenticate_password(password: str) -> None:
    """
    Authenticate the provided password against the stored password in environment variables.

    Args:
        password (str): The password to authenticate.

    Raises:
        HTTPException: If the password is incorrect or missing.
    """
    stored_password = os.getenv("PASSWORD")
    if not stored_password or password != stored_password:
        raise HTTPException(status_code=401, detail="Incorrect password")


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode in the JWT.

    Returns:
        str: Encoded JWT as string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"Access token created with expiration: {expire}")
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token.

    Args:
        data (dict): Data to encode in the JWT.

    Returns:
        str: Encoded JWT as string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"Refresh token created with expiration: {expire}")
    return encoded_jwt


def get_current_user(authorization: str = Header(None)) -> dict:
    """
    Get the current user from the Authorization header.

    Args:
        authorization (str): The Authorization header containing the Bearer token.

    Returns:
        dict: Decoded JWT payload.

    Raises:
        HTTPException: If the Authorization header is missing or invalid.
    """
    if not authorization:
        logger.error("Authorization header missing")
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        logger.error("Invalid authorization format")
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/token/get", response_model=dict)
def login(request: LoginRequest):
    """
    Generate an access and refresh token for the user.

    Args:
        request (LoginRequest): The request containing password for authentication.

    Returns:
        dict: Access token, refresh token, and token type.
    """
    try:
        authenticate_password(request.password)

        access_token = create_access_token(data={"sub": "user"})
        refresh_token = create_refresh_token(data={"sub": "user"})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token/refresh", response_model=dict)
def refresh_token(request: RefreshTokenRequest):
    """
    Generate a new access token using the provided refresh token.

    Args:
        request (RefreshTokenRequest): The request containing the refresh token.

    Returns:
        dict: New access token.
    """
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        new_access_token = create_access_token(data={"sub": "user"})

        return {"access_token": new_access_token}
    except Exception as e:
        logger.error(f"Error during token refresh: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/protected-endpoint", dependencies=[Depends(get_current_user)], response_model=dict)
def protected_endpoint():
    """
    Access a protected endpoint. Requires valid authorization.

    Returns:
        dict: A message indicating successful access to the protected endpoint.
    """
    return {"message": "This is a protected endpoint"}