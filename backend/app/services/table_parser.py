import pdfplumber
from io import BytesIO
from typing import List
from fastapi import UploadFile, HTTPException
import re

def is_valid_date(value: str) -> bool:
    if not value:
        return False
    value = value.strip()
    return bool(re.match(r"^\d{2}[-/]\d{2}[-/]\d{4}$", value))

async def parse_pdf(file: UploadFile) -> List[dict]:
    pdf_bytes = await file.read()
    transactions = []

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text() or ""

        if "Axis Bank" not in text:
            raise HTTPException(status_code=400, detail="Only Axis Bank statements are supported currently.")

        for page in pdf.pages:
            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:
                for row in table:
                    if not row or all(cell is None for cell in row):
                        continue

                    if len(row) < 5:
                        continue

                    date, description, withdrawals, deposits, balance = row[:5]

                    if not is_valid_date(date):
                        continue

                    date = date.strip() if date else ""
                    description = description.strip() if description else ""
                    balance = balance.replace(",", "").strip() if balance else ""

                    try:
                        if withdrawals and withdrawals.strip():
                            amount = -float(withdrawals.replace(",", "").strip())
                            transaction_type = "DEBIT"
                        elif deposits and deposits.strip():
                            amount = float(deposits.replace(",", "").strip())
                            transaction_type = "CREDIT"
                        else:
                            continue

                        transactions.append({
                            "Date": date,
                            "Description": description,
                            "Amount": amount,
                            "TransactionType": transaction_type,
                            "Balance": balance,
                        })
                    except Exception:
                        continue

    return transactions
