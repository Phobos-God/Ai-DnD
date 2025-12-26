from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .routers import auth, characters, parties, actions, story_log, dice_rolls, inventory, level_progression

app = FastAPI(title="AI DnD Backend", description="Backend API for AI Dungeon Master")

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(characters.router, prefix="/api", tags=["characters"])
app.include_router(parties.router, prefix="/api", tags=["parties"])
app.include_router(actions.router, prefix="/api", tags=["actions"])
app.include_router(story_log.router, prefix="/api", tags=["story_log"])
app.include_router(dice_rolls.router, prefix="/api", tags=["dice_rolls"])
app.include_router(inventory.router, prefix="/api", tags=["inventory"])
app.include_router(level_progression.router, prefix="/api", tags=["level_progression"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI DnD Backend"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
