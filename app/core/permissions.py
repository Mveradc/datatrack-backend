from fastapi import Depends, HTTPException
from app.models.user import User
from app.core.auth import get_current_user

def require_verified(current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Your account needs to be verified to perform this action."
        )
    return current_user

def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action."
        )
    return current_user

def require_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only superusers can perform this acction."
        )
    return current_user
