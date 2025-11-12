from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_session
from app.services.author_service import AuthorService
from app.core.response_builder import success_response
from typing import List
from app.schemas.author import AuthorUpdate, AuthorResponse
from app.repositories.author_repository import AuthorRepository

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=List[AuthorResponse], status_code=status.HTTP_200_OK, description="Получение списка авторов с пагинацией")
async def list_authors(
	page: int = Query(1, ge=1, description="Номер страницы"),
	per_page: int = Query(5, ge=1, le=100, description="Количество элементов на странице"),
	session: AsyncSession = Depends(get_session)
):
	author_repo = AuthorRepository(session)
	author_service = AuthorService(author_repo)
	authors = await author_service.get_all(page, per_page)
	return success_response(authors, "Authors fetched successfully")

@router.get("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK, description="Получение автора по id")
async def get_author(author_id: int, session: AsyncSession = Depends(get_session)):
	author_repo = AuthorRepository(session)
	author_service = AuthorService(author_repo)
	author = await author_service.get_by_id(author_id)
	author_data = AuthorResponse.model_validate(author).model_dump()
	return success_response(author_data, "The data was successfully found")

@router.put("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK, description="Обновление автора по id")
async def update_author(author_id: int, author_update: AuthorUpdate, session: AsyncSession = Depends(get_session)):
	author_repo = AuthorRepository(session)
	author_service = AuthorService(author_repo)
	updated_author = await author_service.update(author_id, author_update)
	author_data = AuthorResponse.model_validate(updated_author).model_dump()
	return success_response(author_data, "The data has been successfully updated")

@router.delete("/{author_id}", description="Удаление автора по id")
async def delete_author(author_id: int, session: AsyncSession = Depends(get_session)):
	author_repo = AuthorRepository(session)
	author_service = AuthorService(author_repo)
	await author_service.delete(author_id)
	return success_response({}, "The data has been successfully deleted")
