from app.database.models import async_session, User, Category, Item, Contact, ContactCategory
from sqlalchemy import select, update, delete

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_items_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category_id == category_id))

async def get_item_by_id(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))

async def add_item(name, description, price, category_id, image_url):
    async with async_session() as session:
        session.add(Item(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            image_url=image_url
        ))
        await session.commit()

async def get_contact_categories():
    async with async_session() as session:
        return await session.scalars(select(ContactCategory))

async def get_contacts_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Contact).where(Contact.category_id == int(category_id)))
    
    