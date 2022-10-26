from db.prisma_init import prisma
from prisma.errors import UniqueViolationError


async def create_client(client: dict):
    try:
        client = await prisma.clients.create(data=client)  # type: ignore
    except UniqueViolationError:
        return None
    return client
