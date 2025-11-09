# Backend - Home Irrigation Service

FastAPI-based backend service for smart home irrigation control.

## Setup

### Using UV (recommended)

```bash
cd backend
uv pip install -e .
```

### Using pip

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Running Locally

```bash
cd backend
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Running with Docker

```bash
cd backend
docker build -t irrigation-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data irrigation-backend
```

## API Endpoints

### Status & Monitoring
- `GET /status/metrics` - Current sensor readings and system state

### Control
- `POST /control/mode` - Set auto/manual mode
- `POST /control/valve` - Manual valve control

### Schedule Management
- `GET /schedule/list` - List all schedules
- `POST /schedule/create` - Create new schedule
- `PUT /schedule/{id}` - Update schedule
- `DELETE /schedule/{id}` - Delete schedule
- `POST /schedule/{id}/toggle` - Toggle schedule enabled/disabled

### Configuration
- `GET /config/thresholds` - Get threshold configuration
- `POST /config/thresholds` - Update thresholds

## Database

SQLite database stored in `./data/irrigation.db` (auto-created on first run).

