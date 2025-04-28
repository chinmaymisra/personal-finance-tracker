import pytest
from app.services import parser
from fastapi import UploadFile
from io import BytesIO

class FakeUploadFile:
    """Mock UploadFile object for direct parser testing."""
    def __init__(self, filename, content):
        self.filename = filename
        self.file = BytesIO(content.encode())

    async def read(self):
        return self.file.getvalue()

@pytest.mark.asyncio
async def test_parse_csv_directly():
    csv_content = """Date,Description,Amount,TransactionType,Balance
2025-04-20,Salary Credit,50000,Credit,60000
2025-04-21,Amazon Purchase,-1200,Debit,58800
"""
    fake_file = FakeUploadFile("test.csv", csv_content)

    transactions = await parser.parse_csv(fake_file)

    assert isinstance(transactions, list)
    assert len(transactions) == 2
    assert transactions[0]["Description"] == "Salary Credit"
    assert transactions[1]["Amount"] == -1200  # Might be string depending on pandas read_csv parsing
