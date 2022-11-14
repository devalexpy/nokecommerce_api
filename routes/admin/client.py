from fastapi import (
    APIRouter, status, Depends,
    HTTPException
)
from security import get_admin
from db.admin_queries import get_admin_by_id

router = APIRouter(
    prefix="/admin/client",
    tags=["admin client"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def get_clients(admin=Depends(get_admin)):
    pass
