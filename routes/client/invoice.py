from fastapi import APIRouter, status, Depends
from security import get_user_id


router = APIRouter(
    prefix="/client/invoice",
    tags=["client invoice"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def get_client_invoices(id=Depends(get_user_id)):
    pass
