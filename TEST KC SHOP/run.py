import os
import asyncio
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Проверяем переменные
if not os.getenv('TG_TOKEN'):
    sys.exit("Ошибка: Не найден TG_TOKEN в .env файле!")

# DB_URL не обязателен, т.к. БД по умолчанию 'оригинал.sqlite3'

from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main

async def main():
    # Инициализация БД
    try:
        await async_main()
        print("✅ База данных успешно инициализирована")
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        return

    # Инициализация бота
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
