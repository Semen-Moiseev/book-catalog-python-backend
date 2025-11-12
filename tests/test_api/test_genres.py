import pytest

# # --- Create ---
# @pytest.mark.asyncio
# async def test_create_genre(client: AsyncClient):
# 	payload = {"name": "ЖАНР"}
# 	response = await client.post("/api/genres/", json=payload)
# 	assert response.status_code == 200

# --- Read all ---
@pytest.mark.asyncio
async def test_list_genres(client):
	await client.post("/api/genres/", json={"name": "ЖАНР"})

	response = await client.get("/api/genres/?page=1&per_page=5")
	assert response.status_code == 200

# # --- Read by id ---
# @pytest.mark.asyncio
# async def test_get_genre(client: AsyncClient, genre_fixture: int):
# 	response = await client.get(f"/api/genres/{genre_fixture}")
# 	assert response.status_code == 200

# # --- Update ---
# @pytest.mark.asyncio
# async def test_update_genre(client: AsyncClient, genre_fixture: int):
# 	payload = {"name": "НОВЫЙ ЖАНР"}
# 	response = await client.put(f"/api/genres/{genre_fixture}", json=payload)
# 	assert response.status_code == 200

# # --- Delete ---
# @pytest.mark.asyncio
# async def test_delete_genre(client: AsyncClient, genre_fixture: int):
# 	response = await client.delete(f"/api/genres/{genre_fixture}")
# 	assert response.status_code == 200