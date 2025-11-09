from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from src.app.database.models import Base


_engine: AsyncEngine | None = None
_session_maker: async_sessionmaker[AsyncSession] | None = None


def init_db(database_url: str = "sqlite+aiosqlite:///./irrigation.db") -> None:
    """Initialize the database engine and create tables."""
    global _engine, _session_maker
    _engine = create_async_engine(database_url, echo=False)
    _session_maker = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables() -> None:
    """Create all tables in the database."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Get a database session for dependency injection."""
    if _session_maker is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with _session_maker() as session:
        yield session


def get_engine() -> AsyncEngine:
    """Get the database engine."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _engine

