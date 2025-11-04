from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.api.author_router import router as author_router
from app.api.genre_router import router as genre_router
from app.api.book_router import router as book_router

@asynccontextmanager
async def lifespan(app: FastAPI):
	await init_db()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(author_router, prefix="/api")
app.include_router(genre_router, prefix="/api")
app.include_router(book_router, prefix="/api")