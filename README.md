# Axis Bank Statement Parser

A fullstack application to **upload Axis Bank PDF statements**, **extract transactions** automatically, and **display them cleanly**.

Built using:
- **Frontend**: React + TypeScript (Vite)
- **Backend**: FastAPI (Python)

---

##  Features

- Upload **PDF statements** (only Axis Bank supported currently).
- Extracts:
  - Date
  - Description
  - Amount
  - Transaction Type (Debit/Credit)
  - Balance
- Full **error handling**:
  - Upload non-PDF → Proper error shown
  - Upload corrupted PDF → Proper error shown
  - Upload non-Axis PDF → Proper error shown
- Instant **refresh** on every upload.
- Loading spinner during parsing.
- Clean success/error messages.
- Modern, simple, professional frontend layout.

---

##  Project Structure

```
personal-finance-tracker/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   └── upload.py
│   │   ├── services/
│   │   │   ├── table_parser.py
│   │   │   └── parser.py (fallback text parser)
│   │   └── main.py
│   └── venv/
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── pages/
│   │   │   └── UploadPage.tsx
│   │   └── main.tsx
│   └── index.html
└── README.md
```

---

##  Local Setup Instructions

### Backend (FastAPI)

```bash
cd personal-finance-tracker/backend
python -m venv venv
source venv/Scripts/activate    # (Windows)
pip install fastapi uvicorn pdfplumber pandas
uvicorn app.main:app --reload --port 8000
```

Server will run on: **http://localhost:8000**

---

### Frontend (React + Vite)

```bash
cd personal-finance-tracker/frontend
npm install
npm run dev
```

Frontend will run on: **http://localhost:5173**

---

##  Important Notes

- Currently supports **only Axis Bank** PDF statements.
- Automatically detects and blocks:
  - Non-PDF uploads
  - Broken or corrupted PDFs
  - Non-Axis bank PDFs
- Frontend and backend must run in parallel.

---

## 📈 Future Extensions 

- Add support for multiple banks (HDFC, ICICI, SBI, etc.)
- Add authentication/login for user-specific uploads.
- Expenses prediction using historic data


---