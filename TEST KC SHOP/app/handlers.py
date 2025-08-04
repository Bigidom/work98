from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from urllib.parse import unquote_plus

import app.keyboards as kb
from app.database.requests import (
    set_user,
    get_item_by_id,
    get_contacts_by_category,
    get_feature_values,
    get_items_by_feature,
)

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message): 
    await set_user(message.from_user.id)
    await message.answer(
        'Здравствуйте, вы вошли в магазин Кирпич центр, все цены обновляются и являются реальными',
        reply_markup=kb.menu
    )

@router.callback_query(F.data == "start")   
async def callback_start(callback: CallbackQuery):
    await callback.answer("Вы вернулись в главное меню")
    try:
        await callback.message.edit_text(
            'Добро пожаловать в Кирпич Центр',
            reply_markup=kb.menu
        )
    except Exception:
        await callback.message.answer(
            'Добро пожаловать в Кирпич Центр',
            reply_markup=kb.menu
        )

@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    try:
        await callback.message.edit_text(
            'Выберите характеристику:',
            reply_markup=kb.feature_menu
        )
    except Exception:
        await callback.message.answer(
            'Выберите характеристику:',
            reply_markup=kb.feature_menu
        )

@router.callback_query(F.data.startswith('feature_'))
async def feature_handler(callback: CallbackQuery):
    await callback.answer('')
    feature = callback.data.split('_', 1)[1]
    values = await get_feature_values(feature)
    try:
        await callback.message.edit_text(
            'Выберите значение:',
            reply_markup=kb.feature_values(feature, values)
        )
    except Exception:
        await callback.message.answer(
            'Выберите значение:',
            reply_markup=kb.feature_values(feature, values)
        )

@router.callback_query(F.data.startswith('value_'))
async def feature_value_handler(callback: CallbackQuery):
    await callback.answer('')
    _, feature, value_enc = callback.data.split('_', 2)
    value = unquote_plus(value_enc)
    items = await get_items_by_feature(feature, value)
    try:
        await callback.message.edit_text(
            'Выберите товар:',
            reply_markup=kb.feature_items(feature, value, items)
        )
    except Exception:
        await callback.message.answer(
            'Выберите товар:',
            reply_markup=kb.feature_items(feature, value, items)
        )

@router.callback_query(F.data.startswith('item_'))
async def item_handler(callback: CallbackQuery):
    _, item_id, feature, value_enc = callback.data.split('_', 3)
    value = unquote_plus(value_enc)
    item = await get_item_by_id(int(item_id))
    await callback.answer('')

    if not item:
        await callback.message.answer('Товар не найден')
        return

    text = (
        f"Наименование: {item['name']}\n"
        f"Цена: {item['price']}\n"
        f"Код: {item['code']}\n"
        f"Вид: {item['type']}\n"
        f"Пустотность: {item['emptiness']}\n"
        f"Цвет: {item['color']}\n"
        f"Фактура: {item['texture']}"
    )

    await callback.message.answer(
        text,
        reply_markup=kb.back_to_value(feature, value)
    )

@router.callback_query(F.data == "contacts")
async def contacts_handler(callback: CallbackQuery):
    await callback.answer('')
    try:
        await callback.message.edit_text(
            "Выберите категорию контактов:",
            reply_markup=await kb.contact_categories()
        )
    except Exception:
        await callback.message.answer(
            "Выберите категорию контактов:",
            reply_markup=await kb.contact_categories()
        )

@router.callback_query(F.data.startswith('contact_category_'))
async def contact_category_handler(callback: CallbackQuery):
    category_id = callback.data.split('_')[-1]
    contacts = await get_contacts_by_category(category_id)
    text = ""
    for contact in contacts:
        text += f"Телефон: {contact.phone}\nАдрес: {contact.address}\nПочта: {contact.email}\n"
    await callback.answer('')
    try:
        await callback.message.edit_text(text or "Контакты не найдены.", reply_markup=kb.back_to_contact_categories)
    except Exception:
        await callback.message.answer(text or "Контакты не найдены.", reply_markup=kb.back_to_contact_categories)