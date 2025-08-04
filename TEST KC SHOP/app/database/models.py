import os
from pathlib import Path

from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# Build absolute path to the default SQLite database so that the bot works
# regardless of the current working directory.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
default_db_path = BASE_DIR / "оригинал.sqlite3"
DB_URL = os.getenv('DB_URL', f"sqlite+aiosqlite:///{default_db_path.as_posix()}")
engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25))

class ContactCategory(Base):
    __tablename__ = 'contact_categories'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25))

class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('contact_categories.id'))
    phone: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_category(name):
    async with async_session() as session:
        session.add(Category(name=name))
        await session.commit()

async def add_contact_category(name):
    async with async_session() as session:
        session.add(ContactCategory(name=name))
        await session.commit()

