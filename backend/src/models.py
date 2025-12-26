from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Связь с персонажами
    characters = relationship("Character", back_populates="owner")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    race = Column(String(50), nullable=False)
    character_class = Column(String(50), nullable=False)
    level = Column(Integer, default=1)
    health_points = Column(Integer, default=10)
    max_health_points = Column(Integer, default=10)
    experience = Column(Integer, default=0)
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    constitution = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    wisdom = Column(Integer, default=10)
    charisma = Column(Integer, default=10)
    gold = Column(Integer, default=0)
    description = Column(Text)
    image_url = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Связи
    owner = relationship("User", back_populates="characters")
    party = relationship("Party", back_populates="members")
    inventory_items = relationship("InventoryItem", back_populates="character")
    actions = relationship("CharacterAction", back_populates="character")
    story_log_entries = relationship("StoryLogEntry", back_populates="character")
    dice_rolls = relationship("DiceRoll", back_populates="character")
    level_progression = relationship("LevelProgression", back_populates="character")
    parties = relationship("Party", secondary="party_members", back_populates="members")


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    leader_id = Column(Integer, ForeignKey("characters.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Связи
    leader = relationship("Character", back_populates="party")
    # Обратите внимание: для secondary используется строковое имя таблицы
    members = relationship("Character", secondary="party_members", back_populates="parties")


class PartyMember(Base):
    __tablename__ = "party_members"

    party_id = Column(Integer, ForeignKey("parties.id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Integer, default=1)
    weight = Column(Float, default=0.0)
    value = Column(Integer, default=0)  # стоимость в золотых монетах
    character_id = Column(Integer, ForeignKey("characters.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Связи
    character = relationship("Character", back_populates="inventory_items")


class CharacterAction(Base):
    __tablename__ = "character_actions"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    action_type = Column(String(50), nullable=False)  # attack, spell, skill_check, etc.
    target = Column(String(100))
    roll_result = Column(Integer)
    modifier = Column(Integer)
    total = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связи
    character = relationship("Character", back_populates="actions")


class StoryLogEntry(Base):
    __tablename__ = "story_log"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связи
    character = relationship("Character", back_populates="story_log_entries")


class DiceRoll(Base):
    __tablename__ = "dice_rolls"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    dice_type = Column(String(10), nullable=False)  # d4, d6, d8, d10, d12, d20, d100
    roll_result = Column(Integer, nullable=False)
    modifier = Column(Integer, default=0)
    total = Column(Integer, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связи
    character = relationship("Character", back_populates="dice_rolls")


class LevelProgression(Base):
    __tablename__ = "level_progression"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    level = Column(Integer, nullable=False)
    experience_required = Column(Integer, nullable=False)
    abilities_unlocked = Column(Text)  # JSON or text description of unlocked abilities
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связи
    character = relationship("Character", back_populates="level_progression")
