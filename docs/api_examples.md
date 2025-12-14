# Примеры API запросов и ответов Ai-DnD

Этот документ содержит примеры основных REST-эндпойнтов API, предоставляемых backend-приложением на FastAPI.

## Аутентификация

### POST /api/auth/login

Регистрация или вход игрока в партию.

**Запрос:**
```json
{
  "nickname": "Thorin",
  "party_code": "test123"
}
```

**Ответ (успех):**
```json
{
  "player_id": 1,
  "nickname": "Thorin",
  "party_id": 1,
  "party_code": "test123",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Successfully connected to party"
}
```

**Ответ (ошибка):**
```json
{
  "detail": "Party with code test123 not found"
}
```

## Управление персонажами

### POST /api/characters

Создание нового персонажа.

**Запрос:**
```json
{
  "name": "Thorin Oakenshield",
  "race": "Dwarf",
  "class": "Fighter",
  "level": 1,
  "strength": 16,
  "dexterity": 12,
  "constitution": 15,
  "intelligence": 10,
  "wisdom": 11,
  "charisma": 13,
  "hit_points": 12,
  "max_hit_points": 12,
  "armor_class": 18,
  "player_id": 1
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Thorin Oakenshield",
  "race": "Dwarf",
  "class": "Fighter",
  "level": 1,
  "strength": 16,
  "dexterity": 12,
  "constitution": 15,
  "intelligence": 10,
  "wisdom": 11,
  "charisma": 13,
  "hit_points": 12,
  "max_hit_points": 12,
  "armor_class": 18,
  "player_id": 1,
  "created_at": "2025-12-14T09:00:00"
}
```

### GET /api/characters/{character_id}

Получение информации о персонаже.

**Ответ:**
```json
{
  "id": 1,
  "name": "Thorin Oakenshield",
  "race": "Dwarf",
  "class": "Fighter",
  "level": 1,
  "experience_points": 0,
  "strength": 16,
  "dexterity": 12,
  "constitution": 15,
  "intelligence": 10,
  "wisdom": 11,
  "charisma": 13,
  "hit_points": 12,
  "max_hit_points": 12,
  "temporary_hit_points": 0,
  "armor_class": 18,
  "initiative": 1,
  "speed": 25,
  "player_id": 1,
  "created_at": "2025-12-14T09:00:00",
  "updated_at": "2025-12-14T09:00:00"
}
```

### PATCH /api/characters/{character_id}

Обновление характеристик персонажа (например, после боя).

**Запрос:**
```json
{
  "hit_points": 8,
  "experience_points": 50
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Thorin Oakenshield",
  "race": "Dwarf",
  "class": "Fighter",
  "level": 1,
  "experience_points": 50,
  "strength": 16,
  "dexterity": 12,
  "constitution": 15,
  "intelligence": 10,
  "wisdom": 11,
  "charisma": 13,
  "hit_points": 8,
  "max_hit_points": 12,
  "temporary_hit_points": 0,
  "armor_class": 18,
  "initiative": 1,
  "speed": 25,
  "player_id": 1,
  "created_at": "2025-12-14T09:00:00",
  "updated_at": "2025-12-14T09:05:00"
}
```

## Управление партиями

### GET /api/parties/{party_id}

Получение информации о партии и игроках.

**Ответ:**
```json
{
  "id": 1,
  "code": "test123",
  "created_at": "2025-12-14T08:30:00",
  "is_active": true,
  "players_count": 1,
  "players": [
    {
      "id": 1,
      "nickname": "Thorin",
      "joined_at": "2025-12-14T09:00:00",
      "is_active": true
    }
  ]
}
```

## Взаимодействие с ИИ-ведущим

### POST /api/parties/{party_id}/action

Отправка действия игрока и получение ответа от AI Dungeon Master.

**Запрос:**
```json
{
  "player_id": 1,
  "action_type": "chat_message",
  "message": "Осматриваюсь в поисках тайных дверей"
}
```

**Ответ:**
```json
{
  "response": "Ты внимательно осматриваешь стены и пол. В углу ты замечаешь небольшую трещину в камне, которая выглядит неестественно. Похоже, здесь может быть скрытый механизм.",
  "action_id": 1,
  "timestamp": "2025-12-14T09:10:00"
}
```

### GET /api/parties/{party_id}/story_log

Получение журнала событий партии (история чата).

**Ответ:**
```json
[
  {
    "id": 1,
    "party_id": 1,
    "sender_type": "dm",
    "sender_id": null,
    "message": "Добро пожаловать в подземелье! Вы находитесь в старой заброшенной крепости.",
    "timestamp": "2025-12-14T08:45:00"
  },
  {
    "id": 2,
    "party_id": 1,
    "sender_type": "player",
    "sender_id": 1,
    "message": "Осматриваюсь в поисках тайных дверей",
    "timestamp": "2025-12-14T09:10:00"
  },
  {
    "id": 3,
    "party_id": 1,
    "sender_type": "dm",
    "sender_id": null,
    "message": "Ты внимательно осматриваешь стены и пол. В углу ты замечаешь небольшую трещину в камне, которая выглядит неестественно. Похоже, здесь может быть скрытый механизм.",
    "timestamp": "2025-12-14T09:10:05"
  }
]
```

## Броски кубиков

### POST /api/dice_rolls

Выполнение броска кубика (например, d20 для атаки).

**Запрос:**
```json
{
  "player_id": 1,
  "party_id": 1,
  "dice_type": "d20",
  "modifier": 3,
  "reason": "Attack roll"
}
```

**Ответ:**
```json
{
  "id": 1,
  "player_id": 1,
  "party_id": 1,
  "dice_type": "d20",
  "modifier": 3,
  "result": 14,
  "total": 17,
  "reason": "Attack roll",
  "timestamp": "2025-12-14T09:15:00",
  "message": "Player Thorin rolled d20+3: result 14, total 17"
}
```

## Инвентарь

### GET /api/characters/{character_id}/inventory

Получение инвентаря персонажа.

**Ответ:**
```json
[
  {
    "id": 1,
    "character_id": 1,
    "item_name": "Longsword",
    "quantity": 1,
    "description": "A well-crafted longsword made of steel",
    "weight": 3,
    "value": 15
  },
  {
    "id": 2,
    "character_id": 1,
    "item_name": "Chain Mail",
    "quantity": 1,
    "description": "Well-maintained chain mail armor",
    "weight": 55,
    "value": 75
  },
  {
    "id": 3,
    "character_id": 1,
    "item_name": "Rations",
    "quantity": 5,
    "description": "Days worth of dried food",
    "weight": 2,
    "value": 0.5
  }
]
```

### POST /api/characters/{character_id}/inventory

Добавление предмета в инвентарь.

**Запрос:**
```json
{
  "item_name": "Potion of Healing",
  "quantity": 2,
  "description": "A red potion that restores 2d4+2 hit points",
  "weight": 0.5,
  "value": 50
}
```

**Ответ:**
```json
{
  "id": 4,
  "character_id": 1,
  "item_name": "Potion of Healing",
  "quantity": 2,
  "description": "A red potion that restores 2d4+2 hit points",
  "weight": 0.5,
  "value": 50,
  "created_at": "2025-12-14T09:20:00"
}
```

## Загрузка файлов (MinIO)

### POST /api/upload/map

Загрузка карты в MinIO.

**Запрос (multipart/form-data):**
- file: [binary data of map image]
- filename: "dungeon_map.jpg"
- party_id: 1

**Ответ:**
```json
{
  "filename": "dungeon_map.jpg",
  "url": "/api/maps/dungeon_map.jpg",
  "size": 154230,
  "content_type": "image/jpeg",
  "uploaded_at": "2025-12-14T09:25:00"
}
```

### GET /api/maps/{filename}

Получение карты из MinIO.

Возвращает бинарные данные изображения.

---

Эти примеры демонстрируют основные сценарии взаимодействия с API. Фактические эндпойнты могут варьироваться в зависимости от реализации, но общая структура данных сохраняется.