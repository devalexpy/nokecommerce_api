from fastapi import (
    APIRouter, Body, HTTPException,
    status, Depends, Query
)
from security import get_user_id
from schemas.addresses import (
    AddressBase, AddressesOut, AddressOut,
    AddressUpdate
)
from db.addresses_queries import (
    create_address, get_addresses_by_client_id, update_address_data,
    get_default_address, delete_address
)
from db.clients_queries import get_client_by_id
from prisma.errors import PrismaError


router = APIRouter(
    prefix="/client/address",
    tags=["client address"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=AddressesOut
)
async def get_client_addresses(id=Depends(get_user_id)):
    client = await get_client_by_id(id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    addresses = {"addresses": await get_addresses_by_client_id(id)}
    return addresses


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def add_address(id=Depends(get_user_id), address: AddressBase = Body(...)):
    if await get_client_by_id(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    addresses_data = await get_addresses_by_client_id(id)
    is_default = False
    if not addresses_data:
        is_default = True
    if address.address.lower() in [ad.address.lower() for ad in addresses_data]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address already exists",
        )
    address_data = address.dict()
    address_data["client_id"] = id
    address_data["is_default"] = is_default
    address_data = await create_address(address_data)
    if isinstance(address, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(address_data),
        )

    return {"detail": "Address created successfully"}


@router.put(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=AddressOut
)
async def update_address(id=Depends(get_user_id), address_data: AddressUpdate = Body(...), address_id: str = Query(...)):
    if await get_client_by_id(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    if address_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address id is required",
        )
    new_address = {"address": address_data.new_address}
    address_updated = await update_address_data(new_address)
    if isinstance(address_updated, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(address_updated),
        )

    return address_updated


@router.put(
    path="/default",
    status_code=status.HTTP_200_OK,
)
async def set_default_address(id=Depends(get_user_id), address_id: str = Query(...)):
    if await get_client_by_id(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    default_address = await get_default_address(id)
    if default_address.id == address_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address is already default",
        )
    await update_address_data(default_address.id, {"is_default": False})
    addres_updated = await update_address_data(address_id, {"is_default": True})
    if isinstance(addres_updated, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(addres_updated),
        )
    return {"detail": "Default address updated successfully"}


@router.delete(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def delete_client_address(id=Depends(get_user_id), address_id: str = Query(...)):
    if await get_client_by_id(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    if deleted_address.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't delete default address",
        )
    deleted_address = await delete_address(address_id)
    if isinstance(deleted_address, PrismaError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(deleted_address),
        )
    if deleted_address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    return {"detail": "Address deleted successfully"}
