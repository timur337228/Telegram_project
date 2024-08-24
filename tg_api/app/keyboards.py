from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from tg_api.models.db_helper import get_all_types
from tg_api.func import check_db


async def init_types():
    await check_db()
    types = []

    all_types = await get_all_types()  # Получаем все типы из БД
    button_row = []  # Временный массив для одной строки кнопок

    for i, item in enumerate(all_types):
        button_row.append(KeyboardButton(text=item))  # Создаем кнопку с текстом из базы данных
        if (i + 1) % 3 == 0:
            types.append(button_row)  # Каждые 3 кнопки добавляем в основной массив
            button_row = []  # Очищаем временный массив

    if button_row:
        types.append(button_row)
    # types.append([KeyboardButton(text='Назад ')])

    return ReplyKeyboardMarkup(
        keyboard=types,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Начальное меню',
    )


back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Назад',
)


link_chanel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Крипто Сфера🔮👾', url='https://t.me/crypto_sphere0'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='ссылка на бота',
)

# def get_keyboards(type_product):
#     new_products = []
#     products = get_products_by_type(type_product)
#     for product in products:
#         new_products.append(
#             InlineKeyboardMarkup(
#                 inline_keyboard=[
#                     [
#                         InlineKeyboardButton(text='Скачать👾', url=product.url_download),
#                         InlineKeyboardButton(text='Как работает скрипт?', url=product.url_guide),
#                     ]
#                 ],
#                 resize_keyboard=True,
#                 one_time_keyboard=False,
#             ))
#     return new_products
