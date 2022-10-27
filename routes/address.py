from fastapi import APIRouter, Body, HTTPException, status, Depends
from security import get_user_id
from schemas.addresses import AddressesBase
from db.addresses_queries import get_client_addresses, create_address
from prisma.errors import PrismaError

router = APIRouter(
    prefix="/client/address",
    tags=["client address"]
)


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def add_address(id=Depends(get_user_id), address: AddressesBase = Body(...)):
    addresses_data = await get_client_addresses(id)
    if not addresses_data:
        address.is_default = True
    if address.address.lower() in [ad.address.lower() for ad in addresses_data]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address already exists",
        )
    address_data = address.dict()
    address_data["client_id"] = id
    address_data = await create_address(address_data)
    if isinstance(address, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(address_data),
        )

    return {"message": "Address created successfully"}
