from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from db.prisma_init import prisma
from routes.auth import auth


app = FastAPI()
app.include_router(auth)


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await prisma.disconnect()
