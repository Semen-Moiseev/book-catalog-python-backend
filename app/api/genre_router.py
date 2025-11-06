from fastapi import APIRouter, status, Query
from typing import List
from app.schemas.genre import GenreResponse
from app.services.genre_service import GenreService
from app.core.response_builder import success_response
from app.schemas.genre import GenreCreate, GenreUpdate

router = APIRouter(prefix="/genres", tags=["Genres"])

@router.get("/", response_model=List[GenreResponse], status_code=status.HTTP_200_OK, description="Получение списка жанров с пагинацией")
async def list_genres(
	page: int = Query(1, ge=1, description="Номер страницы"),
	per_page: int = Query(5, ge=1, le=100, description="Количество элементов на странице")
):
	genres = await GenreService.get_all_genres(page, per_page)
	return success_response(genres, "Genres fetched successfully")

@router.get("/{genre_id}", response_model=List[GenreResponse], status_code=status.HTTP_200_OK, description="Получение жанра по id")
async def get_genre(genre_id: int):
	genre = await GenreService.get_by_id_genre(genre_id)
	genre_data = GenreResponse.model_validate(genre).model_dump()
	return success_response(genre_data, "The data was successfully found")

@router.post("/", response_model=List[GenreResponse], status_code=status.HTTP_200_OK, description="Создание нового жанра")
async def create_genre(genre_create: GenreCreate):
	created_genre = await GenreService.create_genre(genre_create)
	genre_data = GenreResponse.model_validate(created_genre).model_dump()
	return success_response(genre_data, "The data has been successfully created")

@router.put("/{genre_id}", response_model=List[GenreResponse], status_code=status.HTTP_200_OK, description="Обновление жанра по id")
async def update_genre(genre_id: int, genre_update: GenreUpdate):
	updated_genre = await GenreService.update_genre(genre_id, genre_update)
	genre_data = GenreResponse.model_validate(updated_genre).model_dump()
	return success_response(genre_data, "The data has been successfully updated")

@router.delete("/{genre_id}", description="Удаление жанра по id")
async def delete_genre(genre_id: int):
	await GenreService.delete_genre(genre_id)
	return success_response({}, "The data has been successfully deleted")