from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import get_current_user
from app.models.filter import Filter
from app.schemas.filter import FilterCreate, FilterOut
from app.schemas.user import UserOut

router = APIRouter(prefix="/filters", tags=["Filters"])

@router.get("/", response_model=FilterOut)
def get_filters(current_user: UserOut = Depends(get_current_user)):
    """
    Retrieve filters for the current user.
    """
    user_filters = Filter.objects(user_id=current_user.id).first()
    if not user_filters:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filters not found")
    
    return user_filters

@router.post("/", response_model=FilterOut)
def create_filter(filter_data: FilterCreate, current_user: UserOut = Depends(get_current_user)):
    """
    Create a new filter for the current user.
    """
    existing_filter = Filter.objects(user_id=current_user.id).first()
    if existing_filter:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filter already exists for this user")
    
    new_filter = Filter(
        user_id=current_user.id,
        filters=filter_data.filters
    )
    new_filter.save()
    
    return new_filter

@router.put("/", response_model=FilterOut)
def update_filter(filter_data: FilterCreate, current_user: UserOut = Depends(get_current_user)):
    """
    Update the filter for the current user.
    """
    existing_filter = Filter.objects(user_id=current_user.id).first()
    if not existing_filter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filter not found")
    
    existing_filter.filters = filter_data.filters
    existing_filter.save()
    
    return existing_filter

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_filter(current_user: UserOut = Depends(get_current_user)):
    """
    Delete the filter for the current user.
    """
    existing_filter = Filter.objects(user_id=current_user.id).first()
    if not existing_filter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filter not found")
    
    existing_filter.delete()
