from db.prisma_init import prisma
from schemas.admins import AdminForQuery


async def get_admin_by_email(email: str):
    admin = await prisma.query_first(
        f"""
        SELECT id, name, last_name, email, phone_number, password , company_name
        FROM admins
        WHERE email = '{email}'
        """,
        model=AdminForQuery,
    )
    return admin
