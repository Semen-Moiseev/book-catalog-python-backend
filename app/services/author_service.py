from app.repositories.author_repository import AuthorRepository

class AuthorService:

	@staticmethod
	async def get_all_authors():
		return await AuthorRepository.get_all()