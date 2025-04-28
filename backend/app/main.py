from fastapi import FastAPI
from app.routers import upload
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Personal Finance Tracker - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL (Vite default port)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)

@app.get("/")
def root():
    return {"message": "Welcome to Personal Finance Tracker Backend"}
