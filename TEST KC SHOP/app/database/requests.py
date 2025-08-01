from app.database.models import async_session, User, Contact, ContactCategory
from sqlalchemy import select, text

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

FEATURE_COLUMNS = {
    "color": "Цвет",
    "type": "Вид",
    "emptiness": "Пустотность",
    "texture": "Фактура",
}

async def get_feature_values(feature_key: str):
    column = FEATURE_COLUMNS.get(feature_key)
    if not column:
        return []
    async with async_session() as session:
        result = await session.execute(text(f'SELECT DISTINCT "{column}" FROM items WHERE "{column}" != ""'))
        return [row[0] for row in result.fetchall()]

async def get_items_by_feature(feature_key: str, value: str):
    column = FEATURE_COLUMNS.get(feature_key)
    if not column:
        return []
    async with async_session() as session:
        result = await session.execute(
            text(f'SELECT rowid, * FROM items WHERE "{column}" = :val'),
            {"val": value}
        )
        return result.fetchall()

async def get_item_by_id(item_id: int):
    async with async_session() as session:
        result = await session.execute(
            text('SELECT rowid, * FROM items WHERE rowid = :id'),
            {"id": item_id}
        )
        row = result.fetchone()
        if not row:
            return None
        keys = result.keys()
        return dict(zip(keys, row))

async def get_contact_categories():
    async with async_session() as session:
        return await session.scalars(select(ContactCategory))

async def get_contacts_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Contact).where(Contact.category_id == int(category_id)))
    
    