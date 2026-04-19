import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.auth.routers import auth, oauth, user
from backend.lessons.routers import languages, lessons, piston
from backend.settings import settings

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

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
)

app.include_router(user.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(oauth.router, prefix="/auth")
app.include_router(languages.router)
app.include_router(lessons.router)
app.include_router(piston.router)


@app.get("/")
def home_page():
    return {"message": "It's Backend"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
