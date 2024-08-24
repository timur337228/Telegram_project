import asyncio
from aiogram import Bot, Dispatcher, F
import asyncio

from tg_api.app.constants import TOKEN, USERNAME
import tg_api.app.keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def start_main_bot():
    from tg_api.admin_app.admin import admin_router
    from tg_api.app.hendlers import main_router
    from tg_api.func import check_db
    await check_db()
    await kb.init_types()
    # dp.include_router(admin_router)
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_main_bot())
    except KeyboardInterrupt:
        print('exit')
