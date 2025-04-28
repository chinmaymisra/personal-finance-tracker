# Backend API Testing Checklist - Personal Finance Tracker

> Version: Phase 1
> Project: Personal Finance Tracker (Million Dollar Project)

---

## 1. Basic Server Health

- [ ] Backend server (`uvicorn`) running without errors
- [ ] `GET /` returns `{"message": "Welcome to Personal Finance Tracker Backend"}`

---

## 2. Upload API `/upload/` Endpoint

- [ ] `POST /upload/` reachable via Insomnia
- [ ] Accepts `multipart/form-data` with key = `file`

---

## 3. File Upload Tests

### 3.1 Positive Tests

- [ ] Upload valid Axis Bank PDF → Receives parsed lines
- [ ] Upload valid Axis Bank CSV → Receives structured JSON

### 3.2 Negative Tests

- [ ] Upload unsupported file (TXT) → 400 Bad Request
- [ ] Upload broken/corrupt file → Graceful error, no crash
- [ ] Upload with wrong field key → Proper validation error

---

## 4. Response Structure

- [ ] Responses always in valid JSON
- [ ] Fields: `transactions`, `detail` are consistently named
- [ ] Proper HTTP Status Codes (e.g., 400 for bad request)

---

## 5. Performance and Limits

- [ ] Handle large files (5–10MB) without server crash
- [ ] Process large PDFs/CSVs within acceptable time limits

---

## 6. Logging and Error Handling

- [ ] Unexpected errors logged clearly (no silent fails)
- [ ] No sensitive file contents printed in logs

---

## Testing Table Template

| Test Case | Expected Result | Actual Result | Pass/Fail |
|:---------:|:---------------:|:-------------:|:---------:|
| Upload Axis Bank CSV | JSON parsed correctly | Pass |
| Upload random .txt file | 400 Bad Request | Pass |
| Upload corrupt PDF | Graceful error | Pass |
| Server handles 5MB file | No crash | Pass |

---
