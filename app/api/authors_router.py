from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_session
from app.schemas.api_response import ApiResponse
from app.schemas.author import AuthorListResponse, AuthorResponse, AuthorUpdate
from app.repositories.author_repository import AuthorRepository
from app.services.author_service import AuthorService


router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=ApiResponse[AuthorListResponse], description="Получение списка авторов с пагинацией")
async def list_authors(
	page: int = Query(1, ge=1, description="Номер страницы"),
	per_page: int = Query(5, ge=1, le=100, description="Количество элементов на странице"),
	session: AsyncSession = Depends(get_session)
):
	repository = AuthorRepository(session)
	service = AuthorService(repository)
	authors_page = await service.list_all(page, per_page)

	return ApiResponse(
		code=200,
		message="The authors were successfully found",
		data=authors_page
	)


@router.get("/{author_id}", response_model=ApiResponse[AuthorResponse], description="Получение автора по id")
async def get_author(author_id: int, session: AsyncSession = Depends(get_session)):
	repository = AuthorRepository(session)
	service = AuthorService(repository)
	author = await service.get_by_id(author_id)

	return ApiResponse(
		code=200,
		message="The author was successfully found",
		data=author
	)


@router.put("/{author_id}", response_model=ApiResponse[AuthorResponse], description="Обновление автора по id")
async def update_author(author_id: int, author_update: AuthorUpdate, session: AsyncSession = Depends(get_session)):
	repository = AuthorRepository(session)
	service = AuthorService(repository)
	updated = await service.update(author_id, author_update)

	return ApiResponse(
		code=200,
		message="The author has been successfully updated",
		data=updated
	)


@router.delete("/{author_id}", response_model=ApiResponse[dict], description="Удаление автора по id")
async def delete_author(author_id: int, session: AsyncSession = Depends(get_session)):
	repository = AuthorRepository(session)
	service = AuthorService(repository)
	await service.delete(author_id)

	return ApiResponse(
		code=200,
		message="The author has been successfully deleted",
		data={}
	)
