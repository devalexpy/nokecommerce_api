from db.prisma_init import prisma
from prisma.errors import PrismaError


async def create_client(client: dict):
    try:
        client = await prisma.clients.create(data=client)
    except PrismaError as error:
        return error
    return client


async def get_client(email: str):
    try:
        client = await prisma.clients.find_unique(where={"email": email})
    except PrismaError as error:
        return error
    return client
