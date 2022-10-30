from turtle import update
from db.prisma_init import prisma
from prisma.errors import PrismaError


async def create_address(address_data: dict):
    try:
        address = await prisma.addresses.create(data=address_data)
    except PrismaError as error:
        return error
    return address


async def get_address_by_id(id):
    address = await prisma.addresses.find_unique(where={"id": id})
    return address


async def get_addresses_by_client_id(id):
    addresses = await prisma.addresses.find_many(where={"client_id": id})
    return addresses


async def update_address_data(id, address_data: dict):
    try:
        address = await prisma.addresses.update(
            where={"id": id},
            data=address_data,
        )
    except PrismaError as error:
        return error
    return address


async def get_default_address(id):
    address = await prisma.addresses.find_first(
        where={
            "AND": [
                {"client_id": id},
                {"is_default": True}
            ]
        }
    )
    return address


async def delete_address(id):
    try:
        address = await prisma.addresses.delete(where={"id": id})
    except PrismaError as error:
        return error
    return address
