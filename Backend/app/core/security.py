from fastapi import Header, HTTPException, status
from typing import Optional


async def get_current_user_id(x_user_id: Optional[int] = Header(None)) -> Optional[int]:
    """
    Placeholder for JWT authentication.
    Currently reads user identity from X-User-Id header.
    TODO: Replace with JWT token validation when auth system is implemented.
    """
    return x_user_id


def verify_user_owns_resource(current_user_id: Optional[int], resource_user_id: int) -> None:
    """
    Validates the authenticated user matches the resource owner.
    No-op when no auth header is present (backwards compatible).
    Raises 403 when header is provided but doesn't match.
    """
    if current_user_id is not None and current_user_id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this rating"
        )
