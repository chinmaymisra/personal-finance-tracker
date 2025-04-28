import pdfplumber
from io import BytesIO
from typing import List
from fastapi import UploadFile
import re

async def parse_pdf(file: UploadFile) -> List[dict]:
    pdf_bytes = await file.read()
    transactions = []
    buffer = ""
    prev_balance = None

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')

            for line in lines:
                line = line.strip()
                if is_valid_transaction_line(line):
                    if buffer:
                        txn = parse_transaction_buffer(buffer, prev_balance)
                        if txn:
                            transactions.append(txn)
                            prev_balance = float(txn["Balance"])
                    buffer = line  # start new transaction buffer
                else:
                    buffer += " " + line  # continuation of previous transaction

            # After page end, parse last buffered transaction
            if buffer:
                txn = parse_transaction_buffer(buffer, prev_balance)
                if txn:
                    transactions.append(txn)
                    prev_balance = float(txn["Balance"])
                buffer = ""

    return transactions

import datetime

def is_valid_transaction_line(line: str) -> bool:
    # Remove leading/trailing spaces first
    line = line.strip()

    # Must strictly start with a date
    match = re.match(r"^(\d{2})-(\d{2})-(\d{4})", line)
    if not match:
        return False

    day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))

    try:
        datetime.date(year, month, day)  # Check if date is a valid calendar date
    except ValueError:
        return False

    # Also, the line must contain at least 2 money-like patterns (amount and balance)
    money_matches = re.findall(r"[\d,]+\.\d{2}", line)
    if len(money_matches) < 2:
        return False

    return True


FORBIDDEN_KEYWORDS = [
    "Int.Pd",
    "Interest Paid",
    "Lien Amount",
    "Relationship Summary",
    "Reward Points",
    "SB:", 
    "Family ID",
    "KYC Status",
    "CRN", 
    "Outstanding Amount",
]

def parse_transaction_buffer(buffer: str, prev_balance: float) -> dict:
    try:
        parts = buffer.split()

        # First part is Date
        date = parts[0]

        # Find all money-like numbers
        money_matches = re.findall(r"[\d,]+\.\d{2}", buffer)

        if len(money_matches) < 2:
            return None  # Not a transaction

        amount = float(money_matches[-2].replace(",", ""))
        balance = float(money_matches[-1].replace(",", ""))

        # Description is everything between date and amount
        amount_idx = buffer.find(money_matches[-2])
        description = buffer[len(date):amount_idx].strip()

        # === New: Filter based on forbidden keywords ===
        if len(description) > 200:
            return None  # Too much garbage

        for keyword in FORBIDDEN_KEYWORDS:
            if keyword.lower() in description.lower():
                return None  # Forbidden keyword detected → garbage line

        # Determine CREDIT or DEBIT
        if prev_balance is not None:
            if balance > prev_balance:
                transaction_type = "CREDIT"
            else:
                transaction_type = "DEBIT"
        else:
            transaction_type = "UNKNOWN"

        if transaction_type == "DEBIT":
            amount = -abs(amount)
        elif transaction_type == "CREDIT":
            amount = abs(amount)

        return {
            "Date": date,
            "Description": description,
            "Amount": amount,
            "TransactionType": transaction_type,
            "Balance": str(balance),
        }
    except Exception:
        return None
