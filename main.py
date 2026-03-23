import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.routers import auth
from backend.auth.routers import user

app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def home_page():
    return {"message": "Привет!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
