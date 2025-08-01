import os
from sqlalchemy import String, BigInteger, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url=os.getenv('DB_URL'), echo=True)
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

class Item(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(512))   
    price: Mapped[int] = mapped_column()
    image_blob: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)  # <-- только это поле!

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