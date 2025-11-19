from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.core.database import init_db
from app.core.exceptions import AppException
from fastapi.responses import JSONResponse
from app.schemas.api_response import ApiErrorResponse
from app.api.authors_router import router as author_router
from app.api.genres_router import router as genre_router
from app.api.books_router import router as book_router

@asynccontextmanager
async def lifespan(app: FastAPI):
	await init_db()
	yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
	return JSONResponse(
		status_code=exc.code,
		content=ApiErrorResponse(
			code=exc.code,
			message=exc.message
		).model_dump()
	)

app.include_router(author_router, prefix="/api")
app.include_router(genre_router, prefix="/api")
app.include_router(book_router, prefix="/api")