import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_upload_non_axis_pdf(async_client):
    with open("app/tests/sample_files/random_non_axis.pdf", "rb") as f:
        response = await async_client.post("/upload/", files={"file": ("random_non_axis.pdf", f, "application/pdf")})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "axis bank" in data["detail"].lower()

@pytest.mark.asyncio
async def test_upload_corrupt_pdf(async_client):
    with open("app/tests/sample_files/corrupt.pdf", "rb") as f:
        response = await async_client.post("/upload/", files={"file": ("corrupt.pdf", f, "application/pdf")})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "corrupted pdf" in data["detail"].lower()
