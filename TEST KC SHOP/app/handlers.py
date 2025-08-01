from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types.input_file import BufferedInputFile

import app.keyboards as kb
from app.database.requests import set_user, get_item_by_id, get_contacts_by_category

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
            'Выберите категорию товара',
            reply_markup=await kb.categories()
        )
    except Exception:
        await callback.message.answer(
            'Выберите категорию товара',
            reply_markup=await kb.categories()
        )

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    category_id = callback.data.split('_')[1]
    try:
        await callback.message.edit_text(
            'Выберите товар по категории',
            reply_markup=await kb.get_items(category_id)
        )
    except Exception:
        await callback.message.answer(
            'Выберите товар по категории',
            reply_markup=await kb.get_items(category_id)
        )

@router.callback_query(F.data.startswith('item_'))
async def item_handler(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    item = await get_item_by_id(item_id)
    await callback.answer('')

    if item.image_blob:
        try:
            photo = BufferedInputFile(item.image_blob, filename="photo.png")
            await callback.message.answer_photo(
                photo,
                caption=f'{item.name}.\n\n{item.description}\n\nЦена: {item.price}',
                reply_markup=await kb.back_to_category(item.category_id)
            )
        except Exception as e:
            print(f"Ошибка при открытии картинки: {e}")
            await callback.message.answer(
                f'Ошибка при открытии картинки!\n{item.name}.\n\n{item.description}\n\nЦена: {item.price}',
                reply_markup=await kb.back_to_category(item.category_id)
            )
    else:
        await callback.message.answer(
            f'{item.name}.\n\n{item.description}\n\nЦена: {item.price}',
            reply_markup=await kb.back_to_category(item.category_id)
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