from fastapi import (
    APIRouter, status, Depends,
    HTTPException, Query
)
from schemas.clients import ClientBase
from security import get_admin
from db.admin_queries import get_admin_by_id
from db.clients_queries import get_all_clients
from typing import List, Optional

router = APIRouter(
    prefix="/admin/client",
    tags=["admin client"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ClientBase]
)
async def get_clients(admin=Depends(get_admin), limit: Optional[int] = Query(None)):
    clients = await get_all_clients(limit)
    if clients is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clients not found",
        )
    return clients
