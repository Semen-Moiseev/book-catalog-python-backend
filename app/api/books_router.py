from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_session
from app.schemas.api_response import ApiResponse
from app.schemas.book import BookListResponse, BookResponse, BookCreate, BookUpdate
from app.repositories.book_repository import BookRepository
from app.repositories.genre_repository import GenreRepository
from app.services.book_service import BookService


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=ApiResponse[BookListResponse], description="Получение списка книг с пагинацией")
async def list_books(
	page: int = Query(1, ge=1, description="Номер страницы"),
	per_page: int = Query(5, ge=1, le=100, description="Количество элементов на странице"),
	session: AsyncSession = Depends(get_session)
) -> ApiResponse:
	repository = BookRepository(session)
	service = BookService(repository)
	books_page = await service.list_all(page, per_page)

	return ApiResponse(
		success=True,
		code=200,
		message="The books were successfully found",
		data=books_page
	)


@router.get("/{book_id}", response_model=ApiResponse[BookResponse], description="Получение книги по id")
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	repository = BookRepository(session)
	service = BookService(repository)
	book = await service.get_by_id(book_id)

	return ApiResponse(
		success=True,
		code=200,
		message="The book was successfully found",
		data=book
	)


@router.post("/", response_model=ApiResponse[BookResponse], description="Создание новой книги")
async def create_book(book_create: BookCreate, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	book_repo = BookRepository(session)
	genre_repo = GenreRepository(session)
	service = BookService(book_repo, genre_repo)
	created = await service.create(book_create)

	return ApiResponse(
		success=True,
		code=200,
		message="The book was successfully created",
		data=created
	)


@router.put("/{book_id}", response_model=ApiResponse[BookResponse], description="Обновление книги по id")
async def update_book(book_id: int, book_update: BookUpdate, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	repository = BookRepository(session)
	service = BookService(repository)
	updated = await service.update(book_id, book_update)

	return ApiResponse(
		success=True,
		code=200,
		message="The book has been successfully updated",
		data=updated
	)


@router.delete("/{book_id}", response_model=ApiResponse[dict], description="Удаление книги по id")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	repository = BookRepository(session)
	service = BookService(repository)
	await service.delete(book_id)

	return ApiResponse(
		success=True,
		code=200,
		message="The book has been successfully deleted",
		data={}
	)