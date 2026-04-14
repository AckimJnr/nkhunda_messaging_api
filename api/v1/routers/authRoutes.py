"""
authRoutes module

Handles user sign-in and sign-out.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import timedelta

from auth.auth import authenticate_user, create_access_token, Token, get_current_active_user
from config.settings import settings
from models.userModel import User

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/signin", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate with email and password.
    Returns a Bearer access token and sets an httpOnly cookie.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@router.post("/signout")
async def signout(current_user: User = Depends(get_current_active_user)):
    """
    Sign out the currently authenticated user by clearing the auth cookie.
    """
    response = JSONResponse(content={"message": "Successfully signed out"})
    response.delete_cookie(key="access_token")
    return response