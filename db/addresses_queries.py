from db.prisma_init import prisma
from prisma.errors import PrismaError


async def create_address(address_data: dict):
    try:
        address = await prisma.addresses.create(data=address_data)
    except PrismaError as error:
        return error
    return address


async def get_client_addresses(id):

    addresses = await prisma.addresses.find_many(where={"client_id": id})
    print(addresses)
    return addresses
