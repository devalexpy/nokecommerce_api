from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from db.prisma_init import prisma
from routes import auth
from routes.client import client, address
from routes.admin import client as admin_client


app = FastAPI()
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(address.router)
app.include_router(admin_client.router)


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await prisma.disconnect()
