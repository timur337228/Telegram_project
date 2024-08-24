import asyncio
from tg_api.models.db_helper import create_product, get_products_by_type, get_all_products, \
    update_product, delete_product_active
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from tg_api.func import check_db
from tg_api.admin_app.constants import ADMIN_ID
import tg_api.admin_app.keyboards as admin_kb

id_del = 0
id_edit = 0
status = ''
edit_b = False
step_edit = ''
step_create = 0
admin_text = [
    'Введите тип вашего товара', 'Введите название вашего товара',
    'Введите описание вашего товара(если ваш товар без описания, введите "null")',
    'Введите цену товара', 'Введите ссылку для скачивания вашего товара(Я диск, Google)',
    'Введите ссылку на телеграм пост, про товар',
    'Товар создается...',
]
admin_router = Router(name='admin')

# Инициализация переменной new_product
new_product = []


@admin_router.message(CommandStart(), F.from_user.id == ADMIN_ID)
async def send_welcome_start(message: Message):
    await check_db()
    await message.answer("Салам, админ", reply_markup=admin_kb.start)


@admin_router.message(F.from_user.id == ADMIN_ID, F.text == 'Изменить товар')
async def send_welcome_create(message: Message):
    global status
    await check_db()
    status = 'edit'
    await message.answer('Введите id товара, который хотите изменить.', reply_markup=admin_kb.back)


@admin_router.message(F.from_user.id == ADMIN_ID, F.text == 'Удалить товар')
async def send_welcome_create(message: Message):
    global status
    await check_db()
    status = 'delete'
    await message.answer('Введите id товара, который хотите удалить.', reply_markup=admin_kb.back)


@admin_router.message(F.from_user.id == ADMIN_ID, F.text == 'Активировать товар')
async def send_welcome_create(message: Message):
    global status
    await check_db()
    status = 'active'
    await message.answer('Введите id товара, который хотите активировать.', reply_markup=admin_kb.back)


@admin_router.message(F.from_user.id == ADMIN_ID, F.text == 'Создать товар')
async def send_welcome_create(message: Message):
    global status
    await check_db()
    status = 'create'
    await message.answer(admin_text[step_create], reply_markup=admin_kb.back)


@admin_router.message(F.from_user.id == ADMIN_ID, F.text == 'Посмотреть все товары, одного типа')
async def send_welcome_create(message: Message):
    global status
    await check_db()
    status = 'see_products_by_type'
    await message.answer('Введите тип товара.', reply_markup=admin_kb.back)


@admin_router.message(F.from_user.id == ADMIN_ID, F.text == 'Посмотреть все товары')
async def send_welcome_create(message: Message):
    await check_db()
    products = await get_all_products()
    if not (products == []):
        await message.reply("Выбери какой скрипт хочешь получить?")
        for product in products:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Скачать👾', url=product.url_download),
                        InlineKeyboardButton(text='Как работает скрипт?', url=product.url_guide),
                    ]
                ],
                resize_keyboard=True,
                one_time_keyboard=False,
            )
            await message.answer(
                f'id: {product.id}\n\n'
                f'Тип: {product.type_product}\n\n'
                f'Название: {product.name.capitalize()}\n\n'
                f'Описание: {product.description.capitalize()}\n\n'
                f'Цена: {product.price}₽\n\n'
                f'Активно: {product.active}\n\n',
                reply_markup=keyboard
            )
    else:
        await message.answer('Ассортимент пуст')


@admin_router.message(F.from_user.id == ADMIN_ID, F.text == 'Назад')
async def send_welcome_back(message: Message):
    global step_create, status, edit_b, step_edit
    await check_db()
    if status == 'create':
        if step_create > 0:
            del new_product[-1]
            step_create -= 1
            await message.answer(admin_text[step_create], reply_markup=admin_kb.back)
        else:
            status = ''
            await message.answer("Салам, админ", reply_markup=admin_kb.start)
    elif status == 'edit':
        if step_edit != '':
            await message.answer('Выберите, что хотите изменить:', reply_markup=admin_kb.edit_product)
            step_edit = ''
        elif edit_b:
            await message.answer('Введите id товара, который хотите изменить.', reply_markup=admin_kb.back)
            edit_b = False
        else:
            status = ''
            await message.answer("Салам, админ", reply_markup=admin_kb.start)
    elif status in ['delete', 'active', 'see_products_by_type']:
        status = ''
        await message.answer("Салам, админ", reply_markup=admin_kb.start)
    # else:
    #     await message.answer("Салам, админ", reply_markup=admin_kb.start)


@admin_router.message(F.from_user.id == ADMIN_ID,
                      F.text.lower().in_(('тип', 'имя', 'описание', 'цена', 'ссылка для скачивания',
                                          'ссылка на пост про скрипт')))
async def send_welcome_back(message: Message):
    await check_db()
    global step_edit
    step_edit = message.text
    await message.answer(f'Введите {message.text.lower()}')
    print(step_edit)


@admin_router.message(F.from_user.id == ADMIN_ID)
async def send_welcome_step(message: Message):
    global step_create, new_product, status, id_edit, edit_b, id_del, step_edit
    await check_db()
    if status == 'create':
        step_create += 1
        await message.answer(admin_text[step_create])
        n = message.text.strip()
        if step_create == 3 and n.lower() == 'null':
            new_product.append(None)
        else:
            new_product.append(n)
        if step_create == 6:
            step_create = 0
            try:
                await create_product(type_product=new_product[0], name=new_product[1], description=new_product[2],
                                     price=int(new_product[3]),
                                     url_download=new_product[4], url_guide=new_product[5])
                await message.answer('Товар успешно создан', reply_markup=admin_kb.start)
                new_product.clear()
            except Exception as e:
                await message.answer(f'Ошибка при создании товара: {e}')
    elif status == 'edit':
        if edit_b is False:
            await message.answer('Выберите, что хотите изменить:', reply_markup=admin_kb.edit_product)
            id_edit = int(message.text)
            edit_b = True
            return
        try:
            if step_edit == 'Тип':
                await update_product(id=id_edit, type=message.text)
                step_edit = ''
            elif step_edit == 'Имя':
                await update_product(id=id_edit, name=message.text)
                step_edit = ''
            elif step_edit == 'Описание':
                await update_product(id=id_edit, description=message.text)
                step_edit = ''
            elif step_edit == 'Цена':
                await update_product(id=id_edit, price=int(message.text))
                step_edit = ''
            elif step_edit == 'Ссылка для скачивания':
                await update_product(id=id_edit, url_download=message.text)
                step_edit = ''
            elif step_edit == 'Ссылка на пост про скрипт':
                await update_product(id=id_edit, url_guide=message.text)
                step_edit = ''
            else:
                return
            await message.answer('Изменения успешно сохранены!')
        except Exception:
            await message.answer('Ошибка при изменение товара')
    elif status == 'delete':
        try:
            await delete_product_active(id=int(message.text), b=False)
            await message.answer('Товар успешно удалён!', reply_markup=admin_kb.start)
            status = ''
        except Exception:
            await message.answer('Ошибка при удалении товара', reply_markup=admin_kb.start)
    elif status == 'active':
        try:
            await delete_product_active(id=int(message.text), b=True)
            await message.answer('Товар успешно активирован!', reply_markup=admin_kb.start)
            status = ''
        except Exception:
            await message.answer('Ошибка при активации товара', reply_markup=admin_kb.start)
    elif status == 'see_products_by_type':
        products = await get_products_by_type(message.text)
        if not (products == []):
            await message.reply("Выбери какой скрипт хочешь получить?")
            for product in products:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text='Скачать👾', url=product.url_download),
                            InlineKeyboardButton(text='Как работает скрипт?', url=product.url_guide),
                        ]
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=False,
                )
                await message.answer(
                    f'id: {product.id}\n\n'
                    f'Тип: {product.type_product}\n\n'
                    f'Название: {product.name.capitalize()}\n\n'
                    f'Описание: {product.description.capitalize()}\n\n'
                    f'Цена: {product.price}₽\n\n'
                    f'Активно: {product.active}\n\n',
                    reply_markup=keyboard
                )
        else:
            await message.answer('Ассортимент пуст')
        status = ''
    else:
        await message.answer('Недопустимая команда', reply_markup=admin_kb.start)
