from fastapi import APIRouter, status
from app.services.author_service import AuthorService
from app.core.response_builder import success_response
from typing import List
from app.schemas.author import AuthorResponse

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", status_code=status.HTTP_200_OK)
async def list_authors():
	authors = await AuthorService.get_all_authors()
	authors_data = [AuthorResponse.model_validate(a).model_dump() for a in authors]
	return success_response(authors_data, "Authors fetched successfully")