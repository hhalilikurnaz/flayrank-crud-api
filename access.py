from fastapi import APIRouter, Header, HTTPException, status

from auth_utils import verify_token


public_router = APIRouter(prefix="/public", tags=["public"])
protected_router = APIRouter(prefix="/protected", tags=["protected"])


@public_router.get("/info")
def public_info():
    return {
        "message": "This is a public endpoint"
    }


@protected_router.get("/profile")
def protected_profile(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    try:
        user = verify_token(token.strip())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {
        "id": user.id,
        "email": user.email,
    }
