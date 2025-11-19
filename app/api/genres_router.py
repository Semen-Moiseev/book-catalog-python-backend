from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_session
from app.schemas.api_response import ApiResponse
from app.schemas.genre import GenreListResponse, GenreResponse, GenreCreate, GenreUpdate
from app.repositories.genre_repository import GenreRepository
from app.services.genre_service import GenreService


router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("/", response_model=ApiResponse[GenreListResponse], description="Получение списка жанров с пагинацией")
async def list_genres(
	page: int = Query(1, ge=1, description="Номер страницы"),
	per_page: int = Query(5, ge=1, le=100, description="Количество элементов на странице"),
	session: AsyncSession = Depends(get_session)
) -> ApiResponse:
	repository = GenreRepository(session)
	service = GenreService(repository)
	genres_page = await service.list_all(page, per_page)

	return ApiResponse(
		success=True,
		code=200,
		message="The genres were successfully found",
		data=genres_page
	)


@router.get("/{genre_id}", response_model=ApiResponse[GenreResponse], description="Получение жанра по id")
async def get_genre(genre_id: int, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	repository = GenreRepository(session)
	service = GenreService(repository)
	genre = await service.get_by_id(genre_id)

	return ApiResponse(
		success=True,
		code=200,
		message="The genre was successfully found",
		data=genre
	)


@router.post("/", response_model=ApiResponse[GenreResponse], description="Создание нового жанра")
async def create_genre(genre_create: GenreCreate, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	repository = GenreRepository(session)
	service = GenreService(repository)
	created = await service.create(genre_create)

	return ApiResponse(
		success=True,
		code=200,
		message="The genre was successfully created",
		data=created
	)


@router.put("/{genre_id}", response_model=ApiResponse[GenreResponse], status_code=status.HTTP_200_OK, description="Обновление жанра по id")
async def update_genre(genre_id: int, genre_update: GenreUpdate, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	repository = GenreRepository(session)
	service = GenreService(repository)
	updated = await service.update(genre_id, genre_update)

	return ApiResponse(
		success=True,
		code=200,
		message="The genre has been successfully updated",
		data=updated
	)


@router.delete("/{genre_id}", response_model=ApiResponse[dict], description="Удаление жанра по id")
async def delete_genre(genre_id: int, session: AsyncSession = Depends(get_session)) -> ApiResponse:
	repository = GenreRepository(session)
	service = GenreService(repository)
	await service.delete(genre_id)

	return ApiResponse(
		success=True,
		code=200,
		message="The genre has been successfully deleted",
		data={}
	)