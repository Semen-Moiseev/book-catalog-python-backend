from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_session
from app.services.book_service import BookService
from app.core.response_builder import success_response
from typing import List
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.repositories.book_repository import BookRepository
from app.repositories.genre_repository import GenreRepository


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Получение списка книг с пагинацией")
async def list_books(
	page: int = Query(1, ge=1, description="Номер страницы"),
	per_page: int = Query(5, ge=1, le=100, description="Количество элементов на странице"),
	session: AsyncSession = Depends(get_session)
):
	book_repo = BookRepository(session)
	book_service = BookService(book_repo)

	books = await book_service.get_all(page, per_page)
	books["items"] = [BookResponse.model_validate({
		"id": book.id,
		"title": book.title,
		"type": book.type,
		"author_id": book.author_id,
		"genres": [genre.id for genre in book.genres]
	}).model_dump() for book in books["items"]]
	return success_response(books, "Books fetched successfully")


@router.get("/{book_id}", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Получение книги по id")
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)):
	book_repo = BookRepository(session)
	book_service = BookService(book_repo)

	book = await book_service.get_by_id(book_id)
	book_data = BookResponse.model_validate({
		"id": book.id,
		"title": book.title,
		"type": book.type,
		"author_id": book.author_id,
		"genres": [genre.id for genre in book.genres]
	}).model_dump()
	return success_response(book_data, "The data was successfully found")


@router.post("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Создание новой книги")
async def create_book(book_create: BookCreate, session: AsyncSession = Depends(get_session)):
	book_repo = BookRepository(session)
	genre_repo = GenreRepository(session)
	book_service = BookService(book_repo, genre_repo)

	created_book = await book_service.create(book_create)
	book_data = BookResponse.model_validate({
		"id": created_book.id,
		"title": created_book.title,
		"type": created_book.type,
		"author_id": created_book.author_id,
		"genres": [genre.id for genre in created_book.genres]
	}).model_dump()
	return success_response(book_data, "The data has been successfully created")


@router.put("/{book_id}", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Обновление книги по id")
async def update_book(book_id: int, book_update: BookUpdate, session: AsyncSession = Depends(get_session)):
	book_repo = BookRepository(session)
	book_service = BookService(book_repo)

	updated_book = await book_service.update(book_id, book_update)
	book_data = BookResponse.model_validate({
		"id": updated_book.id,
		"title": updated_book.title,
		"type": updated_book.type,
		"author_id": updated_book.author_id,
		"genres": [genre.id for genre in updated_book.genres]
	}).model_dump()
	return success_response(book_data, "The data has been successfully updated")


@router.delete("/{book_id}", description="Удаление книги по id")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
	book_repo = BookRepository(session)
	book_service = BookService(book_repo)

	await book_service.delete(book_id)
	return success_response({}, "The data has been successfully deleted")