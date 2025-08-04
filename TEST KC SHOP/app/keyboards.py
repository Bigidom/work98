from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from urllib.parse import quote_plus

from app.database.requests import (
    get_feature_values,
    get_items_by_feature,
    get_contact_categories,
)

# Главное меню
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
    [InlineKeyboardButton(text='Контакты', callback_data='contacts')]
])

# Меню характеристик каталога
feature_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Цвет", callback_data="feature_color")],
    [InlineKeyboardButton(text="Вид", callback_data="feature_type")],
    [InlineKeyboardButton(text="Пустотность", callback_data="feature_emptiness")],
    [InlineKeyboardButton(text="Фактура", callback_data="feature_texture")],
    [InlineKeyboardButton(text="На главную", callback_data="start")],
])

def feature_values(feature, values):
    keyboard = InlineKeyboardBuilder()
    for val in values:
        keyboard.row(
            InlineKeyboardButton(
                text=val,
                callback_data=f"value_{feature}_{quote_plus(val)}"
            )
        )
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="catalog"))
    return keyboard.as_markup()

def feature_items(feature, value, items):
    keyboard = InlineKeyboardBuilder()
    for item in items:
        rowid = item["rowid"]
        name = item["Наименование"]
        keyboard.row(
            InlineKeyboardButton(
                text=name,
                callback_data=f"item_{rowid}_{feature}_{quote_plus(value)}"
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"feature_{feature}"
        )
    )
    return keyboard.as_markup()

def back_to_value(feature, value):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data=f"value_{feature}_{quote_plus(value)}")]
        ]
    )

# Категории контактов
async def contact_categories():
    all_categories = await get_contact_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.row(InlineKeyboardButton(text=category.name, callback_data=f"contact_category_{category.id}"))
    keyboard.row(InlineKeyboardButton(text="На главную", callback_data="start"))
    return keyboard.as_markup()

# Кнопка "Назад" к категориям контактов
back_to_contact_categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="contacts")]
])
