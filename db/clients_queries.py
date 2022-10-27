from pyexpat import model
from select import select
from db.prisma_init import prisma
from prisma.errors import PrismaError


async def create_client(client: dict):
    try:
        client = await prisma.clients.create(data=client)
    except PrismaError as error:
        return error
    return client


async def get_client_by_email(email: str):

    client = await prisma.clients.find_unique(where={"email": email})
    return client


async def get_client_by_id(id):

    client = await prisma.clients.find_unique(
        where={"id": id},
        include={"addresses": True, "invoices": True},
    )
    return client
