from supabase_auth.errors import AuthApiError

from supabase_client import supabase


def verify_token(token: str):
    """Verify a JWT access token with Supabase Auth and return the user."""
    try:
        response = supabase.auth.get_user(token)
    except AuthApiError as exc:
        raise ValueError(exc.message) from exc

    if response is None or response.user is None:
        raise ValueError("Invalid or expired token")

    return response.user
