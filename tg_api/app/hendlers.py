from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from tg_api.func import check_db, check_sub
import tg_api.app.keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_api.models.db_helper import get_products_by_type, get_all_types

main_router = Router(name='main')
types = []


# async def main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     # product_id = await create_product(name='NAME', type_product='Blum', description='s', price=122,
#     #                                   url_download='asdasda', url_guide='asddasd')
#     # print(f"Создан товар с ID: {product_id}")


@main_router.message(CommandStart())
async def send_welcome(message: Message):
    global types
    await check_db()
    for i in await get_all_types():
        types.append(i)
    await message.reply("Привет, этот бот поможет тебе с автоматизацией в крипто играх.💰")
    await message.answer("Выбери игру, по которой хочешь получить софт:",
                         reply_markup=await kb.init_types())


@main_router.message(F.text.in_(types))  # types ['Blum']
async def main_func(message: Message):
    await check_db()
    if await check_sub(message):
        products = await get_products_by_type(message.text)
        if not (products == []):
            await message.reply("Выбери какой скрипт хочешь получить?📱", reply_markup=kb.back)
            for product in products:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text='Скачать!👾', url=product.url_download),
                            InlineKeyboardButton(text='Как работает скрипт?🔮', url=product.url_guide),
                        ]
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=False,
                )
                await message.answer(
                    f'🔥<b>{product.name.capitalize()}</b>\n\n'
                    f'ℹ️<i>{product.description.capitalize()}</i>\n\n'
                    f'💸Цена: <b>{product.price}</b>₽',
                    reply_markup=keyboard,
                    parse_mode='HTML',)
        else:
            await message.answer('Ассортимент пуст😔')
    else:
        await message.answer("Чтобы получить доступ к боту, подпишитесь на наш канал про криптовалюте🔮👾", reply_markup=kb.link_chanel)


@main_router.message(F.text == 'Назад')
async def back(message: Message):
    await message.answer("Выбери игру👾, по которой хочешь получить софт:",
                         reply_markup=await kb.init_types())
