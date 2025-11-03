from fastapi import APIRouter, status, HTTPException
from typing import List
from app.schemas.genre import GenreResponse
from app.services.genre_service import GenreService
from app.core.response_builder import success_response
from app.schemas.genre import GenreCreate, GenreUpdate

router = APIRouter(prefix="/genres", tags=["Genres"])

@router.get("/", response_model=List[GenreResponse], status_code=status.HTTP_200_OK)
async def list_genres():
	genres = await GenreService.get_all_genres()
	genres_data = [GenreResponse.model_validate(genre).model_dump() for genre in genres]
	return success_response(genres_data, "Genres fetched successfully")

@router.get("/{genre_id}", response_model=List[GenreResponse], status_code=status.HTTP_200_OK)
async def get_genre(genre_id: int):
	genre = await GenreService.get_by_id_genre(genre_id)
	if not genre:
		raise HTTPException(status_code=404, detail="Genre not found")

	genre_data = GenreResponse.model_validate(genre).model_dump()
	return success_response(genre_data, "The data was successfully found")

@router.post("/", response_model=List[GenreResponse], status_code=status.HTTP_200_OK)
async def create_genre(genre_create: GenreCreate):
	return await GenreService.create_genre(genre_create)

@router.put("/{genre_id}", response_model=List[GenreResponse], status_code=status.HTTP_200_OK)
async def update_genre(genre_id: int, genre_update: GenreUpdate):
	updated_genre = await GenreService.update_genre(genre_id, genre_update)
	if not updated_genre:
		raise HTTPException(status_code=404, detail="Genre not found")

	genre_data = GenreResponse.model_validate(update_genre).model_dump()
	return success_response(genre_data, "The data has been successfully updated")

@router.delete("/{genre_id}")
async def delete_genre(genre_id: int):
	deleted = await GenreService.delete_genre(genre_id)
	if not deleted:
		raise HTTPException(status_code=404, detail="Genre not found")

	return success_response(None, "The data has been successfully deleted")