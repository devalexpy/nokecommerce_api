from db.prisma_init import prisma
from prisma.errors import PrismaError

from schemas.clients import ClientForQuery


async def create_client(client: dict):
    try:
        client = await prisma.clients.create(data=client)
    except PrismaError as error:
        return error
    return client


async def get_client_by_email(email: str):

    client = await prisma.query_first(
        f"""
        SELECT id, name, last_name, email, phone_number, password
        FROM clients
        WHERE email = '{email}'
        """,
        model=ClientForQuery,
    )
    return client


async def get_client_by_id(id):
    client = await prisma.clients.find_unique(
        where={"id": id}
    )
    return client


async def update_client_data(id, client_data: dict):
    try:
        client = await prisma.clients.update(
            where={"id": id},
            data=client_data
        )
    except PrismaError as error:
        return error
    return client


async def get_all_clients(limit: int = None):
    clients = await prisma.clients.find_many(take=limit)
    return clients
