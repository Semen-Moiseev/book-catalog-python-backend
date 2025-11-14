from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.api.authors_router import router as author_router
from app.api.genres_router import router as genre_router
from app.api.books_router import router as book_router

@asynccontextmanager
async def lifespan(app: FastAPI):
	await init_db()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(author_router, prefix="/api")
app.include_router(genre_router, prefix="/api")
app.include_router(book_router, prefix="/api")