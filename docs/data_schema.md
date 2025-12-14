# Схема данных Ai-DnD

Этот документ описывает структуру базы данных для проекта Ai-DnD, включая таблицы, их поля, типы данных и связи.

## ER-диаграмма (текстовое представление)

```plaintext
+-------------+       +-------------+       +----------------+
|   parties   |       |   players   |       |  characters    |
+-------------+       +-------------+       +----------------+
| id (PK)     |<----->| id (PK)     |<----->| id (PK)        |
| code (UK)   |       | nickname    |       | name           |
| created_at  |       | party_id (FK)|       | race           |
| is_active   |       | joined_at   |       | class          |
+-------------+       +-------------+       | level          |
                                            | experience     |
                                            | str, dex, con, |
                                            | int, wis, cha  |
                                            | hit_points     |
                                            | max_hit_points |
                                            | player_id (FK) |
                                            +----------------+
                                                  |
                                                  |
                                                  v
+----------------+       +----------------+       +----------------+
|  story_log     |       |  actions       |       | character_state|
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | char_id (PK,FK)|
| party_id (FK)  |       | party_id (FK)  |       | current_hp     |
| sender_type    |       | player_id (FK) |       | temp_hp        |
| sender_id      |       | action_type    |       | spell_slots    |
| message        |       | description    |       | conditions     |
| timestamp      |       | timestamp      |       | initiative     |
+----------------+       +----------------+       +----------------+


+----------------+       +----------------+       +----------------+
|  dice_rolls    |       |  inventory     |       |  level_progress|
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| party_id (FK)  |       | char_id (FK)   |       | char_id (FK)   |
| player_id (FK) |       | item_name      |       | level          |
| action_id (FK) |       | quantity       |       | xp_gained      |
| dice_type      |       | description    |       | timestamp      |
| result         |       | weight         |       +----------------+
| total          |       | value          |
| reason         |       | created_at     |
| timestamp      |       +----------------+
+----------------+

+----------------+       +----------------+
|  maps          |       |  sessions      |
+----------------+       +----------------+
| id (PK)        |       | id (PK)        |
| party_id (FK)  |       | party_id (FK)  |
| filename       |       | start_time     |
| url            |       | end_time       |
| uploaded_at    |       | is_completed   |
| content_type   |       +----------------+
| size           |
+----------------+
```

## Описание таблиц

### 1. parties (Партии)

Хранит информацию о игровых сессиях.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| code | VARCHAR(8) (UK) | Уникальный код партии для подключения |
| created_at | TIMESTAMP | Дата и время создания |
| is_active | BOOLEAN | Статус активности партии |
| name | VARCHAR(100) | Название партии (опционально) |

**Индексы:**
- UNIQUE INDEX на `code`
- INDEX на `is_active`

### 2. players (Игроки)

Хранит информацию об игроках в партии.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| nickname | VARCHAR(50) | Имя игрока/персонажа |
| party_id | INTEGER (FK) | Ссылка на партию |
| joined_at | TIMESTAMP | Время подключения |
| is_active | BOOLEAN | Активен ли игрок в данный момент |
| session_token | VARCHAR(255) | Токен сессии для аутентификации |

**Связи:**
- FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE

**Индексы:**
- INDEX на `party_id`
- INDEX на `session_token`

### 3. characters (Персонажи)

Хранит постоянные характеристики персонажа.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| name | VARCHAR(100) | Имя персонажа |
| race | VARCHAR(50) | Раса (Dwarf, Elf, Human и т.д.) |
| class | VARCHAR(50) | Класс (Fighter, Wizard, Rogue и т.д.) |
| level | INTEGER | Текущий уровень |
| experience | INTEGER | Опыт персонажа |
| strength | INTEGER | Сила |
| dexterity | INTEGER | Ловкость |
| constitution | INTEGER | Телосложение |
| intelligence | INTEGER | Интеллект |
| wisdom | INTEGER | Мудрость |
| charisma | INTEGER | Харизма |
| max_hit_points | INTEGER | Максимальные хиты |
| armor_class | INTEGER | Класс доспеха |
| initiative | INTEGER | Инициатива |
| speed | INTEGER | Скорость перемещения |
| hit_dice | VARCHAR(10) | Кубик хитов (1d10, 1d8 и т.д.) |
| player_id | INTEGER (FK) | Ссылка на игрока |
| created_at | TIMESTAMP | Время создания |
| updated_at | TIMESTAMP | Время последнего обновления |

**Связи:**
- FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
- UNIQUE CONSTRAINT на `player_id` (один игрок — один персонаж)

**Индексы:**
- INDEX на `player_id`
- INDEX на `level`
- INDEX на `race`, `class`

### 4. character_state (Состояние персонажа)

Хранит изменяемые параметры персонажа.

| Поле | Тип | Описание |
|------|-----|----------|
| char_id | INTEGER (PK, FK) | Ссылка на персонажа (одновременно PK и FK) |
| current_hp | INTEGER | Текущие хиты |
| temp_hp | INTEGER | Временные хиты |
| spell_slots | JSON | Слоты заклинаний по уровням |
| conditions | JSON | Активные условия (отравление, ослепление и т.д.) |
| exhaustion | INTEGER | Уровень истощения |
| inspiration | BOOLEAN | Есть ли вдохновение |
| last_updated | TIMESTAMP | Время последнего обновления |

**Связи:**
- FOREIGN KEY (char_id) REFERENCES characters(id) ON DELETE CASCADE

### 5. story_log (Журнал событий)

Хранит всю историю общения и повествования.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| party_id | INTEGER (FK) | Ссылка на партию |
| sender_type | VARCHAR(10) | Тип отправителя ("player", "dm", "system") |
| sender_id | INTEGER | ID игрока (null для DM) |
| message | TEXT | Текст сообщения |
| timestamp | TIMESTAMP | Время отправки |
| metadata | JSON | Дополнительные данные (например, тип действия) |

**Связи:**
- FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE

**Индексы:**
- INDEX на `party_id`, `timestamp` (для быстрой выборки по партии и времени)
- INDEX на `sender_type`

### 6. actions (Действия игроков)

Хранит значимые игровые действия.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| party_id | INTEGER (FK) | Ссылка на партию |
| player_id | INTEGER (FK) | Ссылка на игрока |
| action_type | VARCHAR(50) | Тип действия ("chat", "attack", "skill_check", "spell") |
| description | TEXT | Описание действия |
| target | VARCHAR(100) | Цель действия (если есть) |
| timestamp | TIMESTAMP | Время действия |

**Связи:**
- FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE
- FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE

**Индексы:**
- INDEX на `party_id`, `timestamp`
- INDEX на `action_type`

### 7. dice_rolls (Броски кубиков)

Хранит все броски кубиков для прозрачности.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| party_id | INTEGER (FK) | Ссылка на партию |
| player_id | INTEGER (FK) | Ссылка на игрока (null для DM/монстров) |
| action_id | INTEGER (FK) | Ссылка на действие (если связано) |
| dice_type | VARCHAR(20) | Тип кубика ("d20", "d6", "2d8+3") |
| result | INTEGER | Результат броска (без модификатора) |
| modifier | INTEGER | Модификатор |
| total | INTEGER | Итоговый результат (result + modifier) |
| reason | VARCHAR(100) | Причина броска ("attack", "save", "check") |
| timestamp | TIMESTAMP | Время броска |

**Связи:**
- FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE
- FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE SET NULL
- FOREIGN KEY (action_id) REFERENCES actions(id) ON DELETE SET NULL

**Индексы:**
- INDEX на `party_id`, `timestamp`
- INDEX на `player_id`

### 8. inventory (Инвентарь)

Хранит предметы, принадлежащие персонажу.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| char_id | INTEGER (FK) | Ссылка на персонажа |
| item_name | VARCHAR(100) | Название предмета |
| quantity | INTEGER | Количество |
| description | TEXT | Описание предмета |
| weight | DECIMAL(5,2) | Вес предмета |
| value | DECIMAL(8,2) | Стоимость предмета |
| rarity | VARCHAR(20) | Редкость (Common, Uncommon, Rare и т.д.) |
| item_type | VARCHAR(50) | Тип предмета (weapon, armor, potion и т.д.) |
| properties | JSON | Свойства предмета |
| created_at | TIMESTAMP | Время добавления |
| updated_at | TIMESTAMP | Время последнего обновления |

**Связи:**
- FOREIGN KEY (char_id) REFERENCES characters(id) ON DELETE CASCADE

**Индексы:**
- INDEX на `char_id`
- INDEX на `item_type`
- INDEX на `rarity`

### 9. level_progress (Прогресс уровней)

Хранит историю повышения уровней.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| char_id | INTEGER (FK) | Ссылка на персонажа |
| level | INTEGER | Достигнутый уровень |
| xp_gained | INTEGER | Опыт, полученный при повышении |
| level_up_method | VARCHAR(50) | Метод повышения ("manual", "automatic") |
| improvements | JSON | Описание улучшений (выбранные навыки, характеристики) |
| timestamp | TIMESTAMP | Время повышения |

**Связи:**
- FOREIGN KEY (char_id) REFERENCES characters(id) ON DELETE CASCADE

**Индексы:**
- INDEX на `char_id`, `level`
- INDEX на `timestamp`

### 10. maps (Карты)

Хранит информацию о загруженных картах.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| party_id | INTEGER (FK) | Ссылка на партию |
| filename | VARCHAR(255) | Имя файла |
| url | VARCHAR(512) | URL для доступа к карте |
| content_type | VARCHAR(100) | MIME-тип файла |
| size | BIGINT | Размер файла в байтах |
| uploaded_at | TIMESTAMP | Время загрузки |
| description | TEXT | Описание карты |
| is_active | BOOLEAN | Активна ли карта сейчас |

**Связи:**
- FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE

**Индексы:**
- INDEX на `party_id`
- INDEX на `uploaded_at`

### 11. sessions (Игровые сессии)

Хранит информацию о сеансах игры.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| party_id | INTEGER (FK) | Ссылка на партию |
| start_time | TIMESTAMP | Время начала |
| end_time | TIMESTAMP | Время окончания |
| is_completed | BOOLEAN | Завершена ли сессия |
| summary | TEXT | Краткое описание сессии |
| xp_earned | JSON | Опыт, полученный персонажами |

**Связи:**
- FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE

## Схема базы данных в SQL

```sql
-- Создание таблицы parties
CREATE TABLE parties (
    id SERIAL PRIMARY KEY,
    code VARCHAR(8) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Создание таблицы players
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(50) NOT NULL,
    party_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    session_token VARCHAR(255),
    FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE
);

-- Создание индекса для быстрой выборки игроков по партии
CREATE INDEX idx_players_party_id ON players(party_id);

-- Создание таблицы characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    race VARCHAR(50) NOT NULL,
    class VARCHAR(50) NOT NULL,
    level INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    strength INTEGER,
    dexterity INTEGER,
    constitution INTEGER,
    intelligence INTEGER,
    wisdom INTEGER,
    charisma INTEGER,
    max_hit_points INTEGER,
    hit_points INTEGER,
    armor_class INTEGER,
    initiative INTEGER,
    speed INTEGER,
    hit_dice VARCHAR(10),
    player_id INTEGER UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Создание индекса для быстрой выборки персонажей по игроку
CREATE INDEX idx_characters_player_id ON characters(player_id);

-- Создание таблицы character_state
CREATE TABLE character_state (
    char_id INTEGER PRIMARY KEY,
    current_hp INTEGER,
    temp_hp INTEGER DEFAULT 0,
    spell_slots JSON,
    conditions JSON,
    exhaustion INTEGER DEFAULT 0,
    inspiration BOOLEAN DEFAULT false,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (char_id) REFERENCES characters(id) ON DELETE CASCADE
);

-- Создание таблицы story_log
CREATE TABLE story_log (
    id SERIAL PRIMARY KEY,
    party_id INTEGER NOT NULL,
    sender_type VARCHAR(10) NOT NULL CHECK (sender_type IN ('player', 'dm', 'system')),
    sender_id INTEGER,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,
    FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE
);

-- Создание индексов для быстрой выборки по партии и времени
CREATE INDEX idx_story_log_party_timestamp ON story_log(party_id, timestamp);
CREATE INDEX idx_story_log_sender_type ON story_log(sender_type);

-- Создание таблицы actions
CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    party_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    description TEXT,
    target VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Создание индекса для быстрой выборки по партии и времени
CREATE INDEX idx_actions_party_timestamp ON actions(party_id, timestamp);

-- Создание таблицы dice_rolls
CREATE TABLE dice_rolls (
    id SERIAL PRIMARY KEY,
    party_id INTEGER NOT NULL,
    player_id INTEGER,
    action_id INTEGER,
    dice_type VARCHAR(20) NOT NULL,
    result INTEGER NOT NULL,
    modifier INTEGER DEFAULT 0,
    total INTEGER NOT NULL,
    reason VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE SET NULL,
    FOREIGN KEY (action_id) REFERENCES actions(id) ON DELETE SET NULL
);

-- Создание индекса для быстрой выборки по партии и времени
CREATE INDEX idx_dice_rolls_party_timestamp ON dice_rolls(party_id, timestamp);

-- Создание таблицы inventory
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    char_id INTEGER NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INTEGER DEFAULT 1,
    description TEXT,
    weight DECIMAL(5,2),
    value DECIMAL(8,2),
    rarity VARCHAR(20),
    item_type VARCHAR(50),
    properties JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (char_id) REFERENCES characters(id) ON DELETE CASCADE
);

-- Создание индекса для быстрой выборки инвентаря по персонажу
CREATE INDEX idx_inventory_char_id ON inventory(char_id);

-- Создание таблицы level_progress
CREATE TABLE level_progress (
    id SERIAL PRIMARY KEY,
    char_id INTEGER NOT NULL,
    level INTEGER NOT NULL,
    xp_gained INTEGER,
    level_up_method VARCHAR(50),
    improvements JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (char_id) REFERENCES characters(id) ON DELETE CASCADE
);

-- Создание индекса для быстрой выборки прогресса по персонажу и уровню
CREATE INDEX idx_level_progress_char_level ON level_progress(char_id, level);

-- Создание таблицы maps
CREATE TABLE maps (
    id SERIAL PRIMARY KEY,
    party_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    url VARCHAR(512) NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    size BIGINT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE
);

-- Создание индекса для быстрой выборки карт по партии
CREATE INDEX idx_maps_party_id ON maps(party_id);

-- Создание таблицы sessions
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    party_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    is_completed BOOLEAN DEFAULT false,
    summary TEXT,
    xp_earned JSON,
    FOREIGN KEY (party_id) REFERENCES parties(id) ON DELETE CASCADE
);
```

## Примечания

- Все таблицы используют индексы для оптимизации запросов
- Используются внешние ключи для обеспечения целостности данных
- Для текстовых полей с большим объемом данных используется тип TEXT
- JSON поля позволяют хранить гибкие структуры данных (условия, свойства предметов и т.д.)
- Схема спроектирована для масштабируемости и поддержки основных механик D&D 5e
- Миграции базы данных управляются с помощью Alembic

Эта схема данных обеспечивает полное хранение всех аспектов игровой сессии и позволяет эффективно выполнять все необходимые операции приложения Ai-DnD.