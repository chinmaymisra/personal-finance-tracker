import pytest
import os

@pytest.mark.asyncio
async def test_upload_csv(async_client):
    test_csv_path = os.path.join(os.path.dirname(__file__), "sample_files", "sample.csv")

    with open(test_csv_path, "rb") as f:
        response = await async_client.post("/upload/", files={"file": ("sample.csv", f, "text/csv")})
    
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert isinstance(data["transactions"], list)
    assert len(data["transactions"]) == 2  # 2 rows in sample.csv
