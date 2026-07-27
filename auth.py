from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from supabase_auth.errors import AuthApiError

from supabase_client import supabase


router = APIRouter(prefix="/auth", tags=["auth"])


class AuthCredentials(BaseModel):
    email: str
    password: str


def _auth_response(user, session):
    return {
        "user": (
            None
            if user is None
            else {
                "id": user.id,
                "email": user.email,
            }
        ),
        "session": (
            None
            if session is None
            else {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "expires_in": session.expires_in,
                "token_type": session.token_type,
            }
        ),
    }


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: AuthCredentials):
    if not credentials.email.strip() or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required"},
        )

    try:
        result = supabase.auth.sign_up(
            {
                "email": credentials.email.strip(),
                "password": credentials.password,
            }
        )
    except AuthApiError as exc:
        raise HTTPException(
            status_code=exc.status or status.HTTP_400_BAD_REQUEST,
            detail={"error": exc.message},
        ) from exc

    return _auth_response(result.user, result.session)


@router.post("/login")
def login(credentials: AuthCredentials):
    if not credentials.email.strip() or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required"},
        )

    try:
        result = supabase.auth.sign_in_with_password(
            {
                "email": credentials.email.strip(),
                "password": credentials.password,
            }
        )
    except AuthApiError as exc:
        raise HTTPException(
            status_code=exc.status or status.HTTP_401_UNAUTHORIZED,
            detail={"error": exc.message},
        ) from exc

    return _auth_response(result.user, result.session)
