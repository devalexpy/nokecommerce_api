from db.prisma_init import prisma


async def get_admin_by_email(email: str):
    admin = await prisma.admin.find_first(where={"email": email})
    return admin
