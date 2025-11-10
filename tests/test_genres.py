import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_genres():
	async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
		response = await ac.get("/api/genres/?page=1&per_page=5")
	assert response.status_code == 200

	# data = response.json()
	# assert "items" in data
	# assert isinstance(data["items"], list)