# TicTacToeWeb

Веб-приложение **«Крестики-нолики»** на Python (Flask) с многослойной архитектурой и игрой против ИИ на основе алгоритма **минимакс**. Проект в рамках **School 21 / Python_Bootcamp**.

## О проекте

JSON/REST API для игры в крестики-нолики: поддерживает режимы человек против человека, человек против ИИ и ИИ против ИИ. Приложение построено по принципам слоистой (Clean) архитектуры с внедрением зависимостей (DI).

## Структура проекта

```
TicTacToeWeb/
└── src/                          # Исходный код
    ├── app.py                    # Точка входа (Flask)
    ├── requirements.txt          # Зависимости
    ├── web/                      # Слой web (Flask, маршруты, модели, мапперы)
    │   ├── route/game_routes.py  # Эндпоинты игры
    │   ├── module/web_module.py  # Фабрика приложения
    │   ├── model/                # web-модели (dataclass)
    │   └── mapper/               # маппер web ↔ domain
    ├── domain/                   # Слой бизнес-логики (не зависит от фреймворков)
    │   ├── model/                # Board, Game, Player, Symbol
    │   └── service/              # IGameService, GameServiceImpl, Minimax
    ├── datasource/               # Слой хранения (in-memory)
    │   ├── repository/           # GameStorage (thread-safe), GameRepository
    │   ├── model/                # storage-модели (dataclass)
    │   └── mapper/               # маппер domain ↔ storage
    └── di/                       # Контейнер зависимостей (singleton)
        └── container.py
```

## Архитектура

Строгое разделение на четыре слоя, где зависимости направлены внутрь:

- **web** — маршруты, web-модели и мапперы; взаимодействие с внешним миром через HTTP/JSON.
- **domain** — игровая логика: поле 3×3, ходы, проверка победы/ничьей, ИИ.
- **datasource** — потокобезопасное in-memory хранилище игр с маппером.
- **di** — контейнер, собирающий зависимости (storage → repository → service) и внедряющий их в приложение.

## Игровая логика

- Поле **3×3**; символы: `X` (всегда ходит первым) и `O`; `0` — пустая клетка.
- **Минимакс-ИИ** — `Minimax.find_best_move()`: рекурсивный поиск лучшего хода с учётом глубины (победа = `10 - depth`, поражение = `depth - 10`, ничья = 0).
- Полная валидация хода: проверка очереди хода, занятости клетки и неизменности остального поля.
- ИИ-ход выполняется автоматически сразу после хода человека, если следующим ходит бот.
- Параллельные игры: каждая партия хранится по UUID.

## API

| Метод | Путь | Описание |
|---|---|---|
| `POST` | `/game` | Создать игру: `{player_x_name, player_o_name, player_x_is_bot?, player_o_is_bot?}` → `201` |
| `POST` | `/game/<uuid>` | Сделать ход: `{player_id, row, col}` → `200` с состоянием игры, `is_game_over`, `winner_symbol` |

Ошибки возвращаются в формате `ErrorResponse` с кодами `400` (некорректный ход), `404` (игра не найдена), `500` (внутренняя ошибка).

## Запуск

```bash
pip install -r src/requirements.txt
python src/app.py       # или python3
```

По умолчанию сервер стартует на `127.0.0.1:5000`. Настройки через переменные окружения: `FLASK_HOST`, `FLASK_PORT`, `FLASK_DEBUG=true`.

Пример создания игры:

```bash
curl -X POST http://localhost:5000/game \
  -H "Content-Type: application/json" \
  -d '{"player_x_name":"Human","player_o_name":"AI","player_o_is_bot":true}'
```

## Лицензия

School 21 License
