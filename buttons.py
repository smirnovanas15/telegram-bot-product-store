from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, WebAppInfo

cash = KeyboardButton('Наличные')
card = KeyboardButton('Картой онлайн')
ok = KeyboardButton('Подтвердить')
cart_cat = KeyboardButton('Корзина')

back = KeyboardButton('Назад')
order = KeyboardButton('Оформить')
menu = KeyboardButton('Магазин🛍')
back_to_cat = KeyboardButton('<< Вернуться')
message = KeyboardButton('Обратиться к народу')
cl_cart = KeyboardButton('Очистить корзину')

help = KeyboardButton('Помощь🆘')
sale = KeyboardButton('Акции')
ad_category = KeyboardButton('Добавить категорию')
del_dish_b = KeyboardButton('Cписок товаров')
discount = KeyboardButton('Установить скидку')
expenses = KeyboardButton('Внести расходы')
ad_dish = KeyboardButton('Добавить товар')
view_cats = KeyboardButton('Список категорий')
view_dishes = KeyboardButton('Добавить товар')
min_price = KeyboardButton('Минимальный заказ')
number = KeyboardButton('Отправить свой номер', request_contact=True)

main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,row_width=1).add(cart_cat,sale,menu,help)

order_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
order_btn.row(order, back_to_cat, cl_cart)

main_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_btn.row(back)
back_cat = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
back_cat.row(back_to_cat)

admin_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_buttons.add(view_cats, min_price, del_dish_b, message, discount,sale)

admin_cats_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_cats_buttons.row(ad_category, back)

cat_list = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

ready_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ready_button.row(ok)

admin_dishes_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_dishes_buttons.row(back)
user_dishes_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user_dishes_buttons.row(back_to_cat)


async def create_buttons_types(lst, user_role):
    cats = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if user_role == 'admin':
        for name in lst:
            if name not in str(admin_cats_buttons):
                button = KeyboardButton(text=f'{name}')
                cats.row(button)
        else:
            cats.row(ad_category, back)
            return cats
    else:
        for name in lst:
            if name not in str(cat_list):
                button = KeyboardButton(text=f'{name}')
                cat_list.row(button)
        else:
            if "Корзина" not in str(cat_list):
                cat_list.row(cart_cat)
            return cat_list


async def create_buttons_dishes(lst):
    admin_dishes_but = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in lst:
        if name not in str(admin_dishes_buttons):
            button = KeyboardButton(text=f'{name}')
            admin_dishes_but.row(button)
    else:
        admin_dishes_but.row(back, view_dishes)
        return admin_dishes_but


async def user_dishes_buttons(lst):
    user_dishes_but = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in lst:
        if name not in str(admin_dishes_buttons):
            button = KeyboardButton(text=f'{name}')
            user_dishes_but.row(button)
    else:
        user_dishes_but.row(back)
        return user_dishes_but
