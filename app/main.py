from fastapi import FastAPI
from app.api.author_router import router as author_router
from contextlib import asynccontextmanager
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
	await init_db()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(author_router, prefix="/api")