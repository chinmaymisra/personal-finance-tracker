from fastapi import APIRouter, UploadFile, HTTPException
from pdfplumber.utils.exceptions import PdfminerException
from app.services import parser, table_parser

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        transactions = await table_parser.parse_pdf(file)
        if not transactions:
            transactions = await parser.parse_pdf(file)
    except PdfminerException:
        raise HTTPException(status_code=400, detail="Invalid or corrupted PDF file.")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to process the uploaded file. Please upload a valid Axis Bank statement.")

    return {"transactions": transactions}
