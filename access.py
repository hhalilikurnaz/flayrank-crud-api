from fastapi import APIRouter, Depends

from dependencies import get_current_user


public_router = APIRouter(prefix="/public", tags=["public"])
protected_router = APIRouter(prefix="/protected", tags=["protected"])


@public_router.get("/info")
def public_info():
    return {
        "message": "This is a public endpoint"
    }


@protected_router.get("/profile")
def protected_profile(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
    }


@protected_router.get("/dashboard")
def protected_dashboard(user=Depends(get_current_user)):
    return {
        "message": "Dashboard access granted",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }
