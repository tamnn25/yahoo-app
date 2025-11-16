from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.routers import chat, auth, user
from app.routers.draw import crop, graffiti, people_sketch, remove_background, sketch

app = FastAPI(title="FastAPI Chat System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB
init_db()

# Include chat router
app.include_router(chat.router)
app.include_router(user.router)
app.include_router(auth.router)

app.include_router(crop.router)
app.include_router(graffiti.router)
app.include_router(people_sketch.router)
app.include_router(remove_background.router)
app.include_router(sketch.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Chat System"}
