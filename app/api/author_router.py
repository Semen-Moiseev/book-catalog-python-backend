from fastapi import APIRouter, status, HTTPException
from app.services.author_service import AuthorService
from app.core.response_builder import success_response
from typing import List
from app.schemas.author import AuthorResponse
from app.schemas.author import AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=List[AuthorResponse], status_code=status.HTTP_200_OK)
async def list_authors():
	authors = await AuthorService.get_all_authors()
	authors_data = [AuthorResponse.model_validate(a).model_dump() for a in authors]
	return success_response(authors_data, "Authors fetched successfully")

@router.get("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def get_author(author_id: int):
	author = await AuthorService.get_by_id_author(author_id)
	if not author:
		raise HTTPException(status_code=404, detail="Author not found")

	author_data = AuthorResponse.model_validate(author).model_dump()
	return success_response(author_data, "The data was successfully found")

@router.put("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def update_author(author_id: int, author_update: AuthorUpdate):
	updated_author = await AuthorService.update_author(author_id, author_update)
	if not updated_author:
		raise HTTPException(status_code=404, detail="Author not found")

	author_data = AuthorResponse.model_validate(updated_author).model_dump()
	return success_response(author_data, "The data has been successfully updated")

@router.delete("/{author_id}")
async def delete_author(author_id: int):
	deleted = await AuthorService.delete_author(author_id)
	if not deleted:
		raise HTTPException(status_code=404, detail="Author not found")

	return success_response(None, "The data has been successfully deleted")
