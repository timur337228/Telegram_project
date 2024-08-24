from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать товар'),
            KeyboardButton(text='Изменить товар'),
        ],
        [
            KeyboardButton(text='Удалить товар'),
            KeyboardButton(text='Активировать товар'),
        ],
        [
            KeyboardButton(text='Посмотреть все товары, одного типа'),
            KeyboardButton(text='Посмотреть все товары'),
        ],
    ],
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
# null = ReplyKeyboardMarkup(
#     keyboard=[
#         [],
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=False,
#     input_field_placeholder='null',
# )

edit_product = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Тип'),
            KeyboardButton(text='Имя'),
            KeyboardButton(text='Описание'),
        ],
        [
            KeyboardButton(text='Цена'),
            KeyboardButton(text='Ссылка для скачивания'),
            KeyboardButton(text='Ссылка на пост про скрипт'),
        ],
        [
            KeyboardButton(text='Назад'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Назад',
)
