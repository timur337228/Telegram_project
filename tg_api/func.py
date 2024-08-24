import asyncio
from tg_api.models.db_helper import create_product, engine, get_product_by_id, get_products_by_type, get_all_products, \
    update_product, delete_product
from tg_api.models.models import Base
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from main import bot
from tg_api.app.constants import TOKEN, USERNAME


async def check_sub(message: Message):
    await check_db()
    chat_member = await bot.get_chat_member(USERNAME, message.from_user.id)
    return chat_member.status in ['member', 'administrator', 'creator']


async def check_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
