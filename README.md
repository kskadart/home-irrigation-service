
# The Home Irrigation Service

Лёгкий и гибкий клиент–серверный сервис для управления домашним поливом (умный полив грядок / газона) на базе Raspberry Pi.

## Архитектура

- **Backend**: Python 3.12 + FastAPI  
  - чтение датчиков (влажность/температура воздуха, влажность/температура почвы);
  - управление электромагнитным клапаном через MOSFET;
  - автоматический контроллер полива (по порогам, окну времени, дневному лимиту);
  - HTTP API для управления и мониторинга.
- **Frontend**: Next.js (React)  
  - веб‑клиент по Wi‑Fi: дашборд показаний, ручное управление, настройки (планируется).

## Комплектация (основное железо)

**Вычислительная часть**
- Raspberry Pi 4B (4 ГБ ОЗУ).
- microSD 32–64 ГБ (класс A1/A2).

**Питание**
- Блок питания 12 В, 60 Вт, IP67.
- DC–DC преобразователь 12 → 5 В (USB‑C, ≥3 А) для Raspberry Pi.
- Сетевой шнур с вилкой Schuko (3×0.75–1.0 мм²).
- Предохранители:
  - 3 А (линия 12 В → 5 В для Raspberry Pi);
  - 1 А (линия клапана).

**Гидравлика и силовая часть**
- Электромагнитный клапан воды 12 В DC, нормально закрытый (NC), латунь, 1/2".
- MOSFET‑модуль 5–36 В, 15 А (low‑side ключ, вход 3.3 В).
- Диод Шоттки 1N5819 (шунт катушки клапана).
- Электролитический конденсатор 470–1000 µF, ≥25 В (на линии 12 В у клапана).

**Датчики**
- SHT31‑D — датчик температуры и влажности воздуха (I²C, 3.3 В).
- DS18B20 — герметичный датчик температуры почвы (1‑Wire).
- Датчик влажности/температуры почвы с аналоговым выходом 0–10 В, IP68.
- ADS1115 — 16‑битный АЦП (I²C, 3.3 В) для чтения 0–10 В датчика через делитель.

## Функционал

### Backend (FastAPI)
- ✅ Чтение датчиков температуры и влажности (воздух + почва)
- ✅ Управление электромагнитным клапаном
- ✅ Автоматический контроллер с динамическими порогами
- ✅ Календарное планирование полива
- ✅ HTTP API для управления и мониторинга
- ✅ SQLite база данных для конфигурации и истории
- ✅ Мокирование железа для разработки

### Frontend (Next.js)
- ✅ Мобильный дашборд с real-time данными
- ✅ Ручное управление клапаном
- ✅ Переключение режимов (auto/manual)
- ✅ Настройка порогов полива
- ✅ Управление расписанием полива
- ✅ Адаптивный дизайн для смартфонов

## Быстрый старт с Docker (рекомендуется)

### Запуск всей системы

```bash
# Клонировать репозиторий
git clone <repo-url>
cd home-irrigation-service

# Запустить backend + frontend
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

Сервисы будут доступны:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Остановка

```bash
docker-compose down
```

## Разработка локально

### Backend

```bash
cd backend

# Установить зависимости с UV
uv pip install -e .

# Запустить сервер
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd client

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev
```

## API Эндпоинты

### Статус и мониторинг
- `GET /status/metrics` — текущие показания датчиков и состояние

### Управление
- `POST /control/mode` — переключение режима `auto` / `manual`
- `POST /control/valve` — ручное управление клапаном

### Конфигурация
- `GET /config/thresholds` — получить пороги
- `POST /config/thresholds` — обновить пороги

### Расписание
- `GET /schedule/list` — список всех расписаний
- `POST /schedule/create` — создать расписание
- `PUT /schedule/{id}` — обновить расписание
- `DELETE /schedule/{id}` — удалить расписание
- `POST /schedule/{id}/toggle` — включить/отключить расписание

Полная документация API: http://localhost:8000/docs

## Web‑клиент (Next.js)

Адаптивное веб-приложение с функциями:
- Отображение температуры и влажности (воздух + почва)
- Индикатор состояния клапана и режима работы
- Ручное управление клапаном
- Настройка порогов полива
- Календарное планирование
- Оптимизировано для смартфонов

Доступ с мобильного устройства:
```
http://<raspberry-pi-ip>:3000
```

## База данных

SQLite база данных создается автоматически при первом запуске:
- Путь: `./backend/data/irrigation.db`
- Таблицы: schedules, thresholds, sensor_readings
- Персистентность через Docker volume

## Структура проекта

```
home-irrigation-service/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   └── app/
│   │       ├── api/        # API routes
│   │       ├── database/   # SQLAlchemy models
│   │       ├── hardware/   # Sensor/valve interfaces
│   │       └── services/   # Business logic
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
├── client/                  # Next.js frontend
│   ├── src/
│   │   ├── app/           # Pages
│   │   ├── components/    # React components
│   │   └── lib/           # API client
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Развертывание на Raspberry Pi

```bash
# 1. Клонировать на RPi
git clone <repo-url>
cd home-irrigation-service

# 2. Установить Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Запустить
docker-compose up -d

# 4. Настроить автозапуск
sudo systemctl enable docker
```

Доступ с локальной сети:
- Web UI: `http://<raspberry-pi-ip>:3000`
- API: `http://<raspberry-pi-ip>:8000`
