from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from pathlib import Path

BASE = Path.cwd()
DB_PATH = BASE / "db.sqlite3"

engine = create_async_engine(url=f'sqlite+aiosqlite:///{DB_PATH}')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass    


class UserLocation(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)

    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    forecast_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    notify_time: Mapped[str | None] = mapped_column(String(5), nullable=True)
    user_timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)