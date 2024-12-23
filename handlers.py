import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from buttons import *
from cart import create_id_dish, user_cart, cart_cr, clear_cart, compiration_prices, total
from config import admins_IDS
from data import add_dish_cat_to_base, get_all_categories, add_dish_to_base, get_cat_list, get_dish_with_type, \
    set_min_order, get_min_order, get_all_dishes, get_dish_list, remove_dish, remove_cat, \
    save_subscribe_id, get_subscribes_id, set_discount, get_discount, get_dish, get_sale, edit_sale

from main import dp, bot

info_about_new_dish = []
info_about_new_order = {}
about_order = {}
new_message = []


class expenses(StatesGroup):
    count = State()
    title = State()


class get_info_about_order(StatesGroup):
    person_name = State()
    person_number = State()
    person_adres = State()
    person_payment = State()
    order_comment = State()


class add_dish(StatesGroup):
    title_dish = State()
    category_dish = State()
    price_dish = State()
    structure_dish = State()
    weight_dish = State()
    photo_dish = State()


class Sale(StatesGroup):
    edit = State()


class add_cats(StatesGroup):
    title = State()


class create_message(StatesGroup):
    message = State()
    photo = State()


class discount_st(StatesGroup):
    coast = State()


class min_order(StatesGroup):
    price = State()


@dp.message_handler(commands=['start'])  # Сообщение при старте бота
async def start_message(message: types.message):
    print('алло')
    info_about_new_dish.clear()
    await save_subscribe_id(str(message.from_id))
    await get_subscribes_id()
    for ids in admins_IDS:
        if message.from_id == int(ids):  # Сообщение для админа
            await message.answer(text='Вы авторизованы как администратор.', reply_markup=admin_buttons)
            break
    else:
        await message.answer(text=f'Приветствуем вас в продуктовом магазине Якорек!\n'
                                  f'С помощью данного бота вы сможете оформить заказ на доставку!\n'
                                  f'-Доставка работает ТОЛЬКО в черте города.\n'
                                  f'-Минимальная сумма заказа {await get_min_order()} RUB.\n'
                                  f'Хорошего дня! Мы всегда рады вас видеть!\n'
                                  f'Вы так же можете связаться с нами по номеру +79108859900\n'
                                  f'Для продолжения нажмите кнопку "Ознакомиться с меню."',
                             reply_markup=main)


@dp.message_handler()
async def worked_with_buttons(message: types.Message, state: FSMContext):
    cats = await get_cat_list()
    dishes = await get_dish_list()
    answer = message.text
    if answer == 'Установить скидку':
        if await get_discount() > 0:
            await message.answer(text=f'Сейчас ВКЛЮЧЕНА скидка {await get_discount()}%\n'
                                      'Введите НОВЫЙ процент скидки:\n'
                                      'Чтобы ВЫКЛЮЧИТЬ скидку введите 0', reply_markup=main_btn)
            await discount_st.coast.set()
        else:
            await message.answer(text=f'Сейчас скидка ВЫКЛЮЧЕНА\n'
                                      'Введите процент скидки:\n', reply_markup=main_btn)
            await discount_st.coast.set()
    if answer == 'Магазин🛍' or answer == '<< Вернуться':
        await get_all_categories('user')
        await message.answer(text='Выбор категории:', reply_markup=cat_list)
    if answer == 'Список категорий':
        await message.answer(text=f'Все добавленные категории:\n'
                                  'ЧТО БЫ УДАЛИТЬ КАТЕГОРИЮ, НАЖМИ НА НЕЁ',
                             reply_markup=await get_all_categories('admin'))
    if answer == 'Добавить категорию':
        await message.answer(text='Введите название:')
        await add_cats.title.set()
    if answer == 'Акции':
        if str(message.from_user.id) in admins_IDS:
            await message.answer(f'Информация об акциях сейчас:\n\n'
                                 f'{await get_sale()}\n\n'
                                 f'Вы можете ввести новую информацию либо нажмите назад', reply_markup=main_btn)
            await Sale.edit.set()
        else:
            await message.answer(text=await get_sale(),reply_markup=main)
    if 'Помощь' in answer:
        await message.answer(f'Если у вас возникли вопросы вы можете связаться с нашим менеджером:\n'
                             f'https://t.me/AnastasiaS1501',reply_markup=main)
    if answer == 'Обратиться к народу':
        for ids in admins_IDS:
            if message.from_id == int(ids):
                await message.answer(text='Напишите сообщение для подписчиков: ', reply_markup=main_btn)
                await create_message.message.set()
    if answer == 'Назад':
        await state.finish()
        for ids in admins_IDS:
            admin_dishes_buttons.clean()
            if message.from_id == int(ids):  # Сообщение для админа
                await message.answer(text='Вы авторизованы как администратор.', reply_markup=admin_buttons)
                break
        else:
            await message.answer(text=f'Приветствуем вас в продуктовом магазине Якорек!"\n'
                                      f'С помощью данного бота вы сможете оформить заказ на доставку!\n'
                                      f'-Доставка работает ТОЛЬКО в черте города.\n'
                                      f'-Минимальная сумма заказа {await get_min_order()} RUB.\n'
                                      f'Хорошего дня! Мы всегда рады вас видеть!\n'
                                      f'Вы так же можете связаться с нами по номеру +79108859900\n'
                                      f'Для продолжения нажмите кнопку "Ознакомиться с меню."',
                                 reply_markup=main)  # type: ignore
    if answer == 'Добавить товар':
        await message.answer(text='Введите название товара:', reply_markup=main_btn)
        await add_dish.title_dish.set()
    if answer in cats:
        dishes_u = await get_dish_with_type(answer)
        if str(message.from_id) in admins_IDS:
            await remove_cat(answer)
            await message.answer(f'Категория {answer} удалена!', reply_markup=await get_all_categories('admin'))
        else:
            dishes_lst = []
            count_dish = 0
            for key, value in dishes_u.items():
                dishes_lst.append(key)
                count_dish += 1

            else:
                if count_dish == 0:
                    await message.answer(f'В этой категории пока нет данного товара:(\n'
                                         f'Но мы исправимся, правда.',
                                         reply_markup=await get_all_categories('user'))
                else:
                    await message.answer(text='Выберите товар:', reply_markup=await user_dishes_buttons(dishes_lst))
    if 'Корзина' in answer:
        cart_result = await cart_cr(message.from_user.id)
        if cart_result is False:
            await message.answer(text='Корзина пуста', reply_markup=main)
    if answer in dishes:
        if str(message.from_id) in admins_IDS:
            await remove_dish(answer)
            await message.answer(text=f'Товар {answer} удален!', reply_markup=await get_all_dishes())
        else:
            print('Показ позиции')
            dish_info = await get_dish(answer)
            add_but = InlineKeyboardButton('В корзину', callback_data=f'add_{dish_info[0][0]}')
            add_to_cart = InlineKeyboardMarkup().add(add_but)
            if await get_discount() <= 0:
                await message.answer(text=f'{dish_info[0][1]}', reply_markup=back_cat)
                await message.answer_photo(photo=dish_info[0][7], caption=f'Состав:{dish_info[0][5]}\n'
                                                                          f'Вес/Объём:{dish_info[0][6]}\n'
                                                                          f'Стоимость:{dish_info[0][4]} RUB\n',
                                           reply_markup=add_to_cart)
            else:
                discount = await get_discount()
                await message.answer(text=f'{dish_info[0][1]}', reply_markup=back_cat)
                await message.answer_photo(photo=dish_info[0][7], caption=f'Состав:{dish_info[0][5]}\n'
                                                                          f'Вес/Объём:{dish_info[0][6]}\n'
                                                                          f'Стоимость:{round(float(dish_info[0][4]) * (1 - discount / 100), 2)} RUB\n',
                                           reply_markup=add_to_cart)

    if answer == 'Оформить':
        if await compiration_prices(message.from_user.id):
            await bot.send_message(chat_id=message.from_user.id, text='Заканчиваем оформление заказа\nВведите имя:',
                                   reply_markup=main_btn)
            await get_info_about_order.person_name.set()
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'Минимальная сумма заказа {await get_min_order()} RUB',
                                   reply_markup=order_btn)
    if answer == 'Очистить корзину':
        await clear_cart(message.from_id)
        await get_all_categories('user')
        await message.answer(text='Корзина очищена!', reply_markup=cat_list)
    if answer == 'Подтвердить':
        await send_order_to_restouran(info_about_new_order, about_order, message.from_user.id)
        await clear_cart(message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id,
                               text='Спасибо за заказ!\nЖдём вас снова!\nЧто бы снова сделать заказ нажмите кнопку ниже.',
                               reply_markup=main)  # type: ignore
    if answer == 'Минимальный заказ':
        for ids in admins_IDS:
            if message.from_id == int(ids):
                await message.answer(text=f'УСТАНОВЛЕННАЯ минимальная сумма заказа {await get_min_order()} RUB\n'
                                          f'Введите НОВУЮ минимальную сумму заказа RUB: ', reply_markup=main_btn)
                await min_order.price.set()
    if answer == 'Cписок товаров':
        for ids in admins_IDS:
            if message.from_id == int(ids):
                await get_all_dishes()
                await message.answer(text=f'Список всех товаров: \n'
                                          f'ЧТО БЫ УДАЛИТЬ ТОВАР, НАЖМИ НА НЕГО!', reply_markup=await get_all_dishes())


@dp.message_handler(state=Sale.edit)
async def edit_sale_fc(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer(text='Вы авторизованы как администратор.', reply_markup=admin_buttons)
        await state.finish()
    else:
        await edit_sale(await get_sale(), message.text)
        await message.answer(text=f'Вы изменили текст акций', reply_markup=admin_buttons)
        await state.finish()


@dp.message_handler(state=expenses.count)
async def create_message_text(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await message.answer(text='Вы авторизованы как администратор.', reply_markup=admin_buttons)
        await state.finish()
    else:
        if ',' in answer:
            answer = answer.replace(',', '.')
        await state.update_data(count=float(answer))
        await message.answer(f'Сумма {answer} RUB введена.\n'
                             f'Введите наименование:', reply_markup=main_btn)
        await expenses.title.set()


@dp.message_handler(state=expenses.title)
async def create_message_text(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await message.answer('Введите СУММУ:', reply_markup=main_btn)
        await expenses.count.set()
    else:
        await state.update_data(title=answer)
        data = await state.get_data()
        await add_expense(data)  # type: ignore
        await message.answer(f'Получается вы потратили {data["count"]} RUB на {data["title"]}?\n'
                             f'Нам очень грустно', reply_markup=admin_buttons)
        await state.finish()


@dp.message_handler(state=create_message.message)
async def create_message_text(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        new_message.append(answer)
        await message.answer(text='Теперь добавьте фото для поста: ', reply_markup=main_btn)
        await create_message.photo.set()


@dp.message_handler(content_types=['photo'], state=create_message.photo)
async def create_message_photo(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        answer = message.photo[0].file_id
        new_message.append(answer)
        await message.answer(text=f'Сообщение отправлено!\n'
                                  f'Получило {await send_messages_subscribes(new_message)} человек(а)!',
                             reply_markup=main_btn)
        print(f'Отправлено сообщение для {await send_messages_subscribes(new_message)} человек(а)')
        new_message.clear()
        await state.finish()


@dp.message_handler(state=min_order.price)
async def deli_price_set(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        await set_min_order(answer)
        await message.answer(text=f'Минимальная стоимость заказа теперь {answer} RUB', reply_markup=admin_buttons)
        print(f'Изменена стоимость минимальная стоимость заказа {answer} RUB')
        await state.finish()


@dp.message_handler(state=discount_st.coast)
async def discount_set(message: types.Message, state: FSMContext):
    lst_discount = []
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    elif int(answer) > 0:
        lst_discount.append('yes')
        lst_discount.append(answer)
        await message.answer(text=f'Скидка в размере {answer}% ВКЛЮЧЕНА!', reply_markup=admin_buttons)
        await set_discount(lst_discount)
        print(f'Включена скидка в размере {answer} %')
        await state.finish()
    else:
        lst_discount.append('no')
        lst_discount.append(answer)
        await message.answer(text=f'Скидка ВЫКЛЮЧЕНА!', reply_markup=admin_buttons)
        await set_discount(lst_discount)
        print('Выключена скидка')
        await state.finish()


@dp.message_handler(state=add_cats.title)
async def add_category(message: types.Message, state: FSMContext):
    answer = message.text
    await add_dish_cat_to_base(answer)
    await message.answer(text=f'Категория {answer} добавлена!', reply_markup=admin_buttons)
    await state.finish()


@dp.message_handler(state=add_dish.title_dish)
async def add_dish_name(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        info_about_new_dish.append(answer)
        await get_all_categories('admin')
        await message.answer(text=f'Выберите категорию', reply_markup=await get_all_categories('admin'))
        await add_dish.category_dish.set()


@dp.message_handler(state=add_dish.category_dish)
async def add_dish_cat(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        info_about_new_dish.append(answer)
        await message.answer(text=f'Введите стоимость RUB', reply_markup=main_btn)
        await add_dish.price_dish.set()


@dp.message_handler(state=add_dish.price_dish)
async def add_dish_price(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        info_about_new_dish.append(answer)
        await message.answer(text=f'Состав:', reply_markup=main_btn)
        await add_dish.structure_dish.set()


@dp.message_handler(state=add_dish.structure_dish)
async def add_dish_structure(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        info_about_new_dish.append(answer)
        await message.answer(text=f'Вес:', reply_markup=main_btn)
        await add_dish.weight_dish.set()


@dp.message_handler(state=add_dish.weight_dish)
async def add_dish_weight(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        info_about_new_dish.append(answer)
        await message.answer(text=f'А теперь фото:', reply_markup=main_btn)
        await add_dish.photo_dish.set()


@dp.message_handler(content_types=['photo'], state=add_dish.photo_dish)
async def add_dish_photo(message: types.Message, state: FSMContext):
    answer = message.photo[0].file_id
    info_about_new_dish.append(answer)
    info_about_new_dish.insert(2, 'yes')
    await message.answer(text=f'Товар добавлен!', reply_markup=admin_buttons)
    await state.finish()
    await add_dish_to_base(info_about_new_dish)
    info_about_new_dish.clear()


@dp.callback_query_handler()
async def callback_process(call: types.CallbackQuery, state: FSMContext):
    await call.answer('ок')
    print('Хендлер')
    if 'add_' in str(call.data):
        print('Добавили')
        cart_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        cart_btn.clean()
        await create_id_dish(str(call.from_user.id), str(call.data))
        cart = KeyboardButton(f'Корзина({round(user_cart[str(call.from_user.id)]["Итог"], 2)} RUB)')
        cart_btn.row(cart, back_to_cat, cl_cart)
        await call.answer(text='Добавлено успешно!')
        await bot.send_message(chat_id=call.from_user.id, text='Позиция добавлена', reply_markup=cart_btn)
    elif 'accept' in str(call.data):
        order_number = str(call.data)[7:10]
        await bot.send_message(chat_id=call.from_user.id, text=f'Заказ {order_number} поступил в обработку!')
        await send_order_to_restouran(info_about_new_order, about_order, call.from_user.id)
        await clear_cart(call.from_user.id)
        await call.answer(text='Заказ в обработке!')
    elif 'invite' in str(call.data):
        await bot.send_message(chat_id=str(call.data)[11:], text=f'Ваш заказ #{str(call.data)[7:10]} принят!\n'
                                                                 f'Мы скоро с вами свяжемся!\n'
                                                                 f'Спасибо за заказ! Ждём вас снова!',
                               reply_markup=main)  # type: ignore
        await bot.send_message(chat_id=call.from_user.id, text=f'Вы ПРИНЯЛИ заказ #{str(call.data)[7:10]}')
        await call.answer(text='Заказ принят!')


@dp.callback_query_handler(state=get_info_about_order.order_comment)
async def callback_comment(call: types.CallbackQuery, state: FSMContext):
    if 'No_' in str(call.data):
        info_about_new_order[str(call.from_user.id)]['comment'] = '-'
        await state.finish()
        await call.answer(text='Принято')
        # Предчек
        order_number = random.randint(100, 999)
        add_butt = InlineKeyboardButton('Подтвердить заказ',
                                        callback_data=f'accept_{order_number}_{call.from_user.id}')
        accept_but = InlineKeyboardMarkup().add(add_butt)
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'Номер вашего заказа {order_number}\n{about_order[str(call.from_user.id)]["info"]}\nАдрес доставки {info_about_new_order[str(call.from_user.id)]["adres"]}\nОплата наличными курьеру\nКомментарий к заказу: {info_about_new_order[str(call.from_user.id)]["comment"]}',
                               reply_markup=accept_but)
        about_order[str(call.from_user.id)]['order_number'] = order_number


async def create_cart(info, chat_id, total):
    await bot.send_message(chat_id=chat_id, text=f'Ваш заказ:\n{info}', reply_markup=order_btn)
    about_order[str(chat_id)] = {'info': info,
                                 'total': total}


@dp.message_handler(state=get_info_about_order.person_name)
async def get_name(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await start_message(message)
        await state.finish()
    else:
        info_about_new_order[str(message.from_user.id)] = {}
        info_about_new_order[str(message.from_user.id)]['name'] = answer
        info_about_new_order[str(message.from_user.id)]['who'] = message.from_user.username
        number_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        number_btn.row(number)
        await bot.send_message(chat_id=message.from_user.id, text='Введите номер телефона:', reply_markup=number_btn)
        await get_info_about_order.person_number.set()


@dp.message_handler(content_types=['contact'], state=get_info_about_order.person_number)
@dp.message_handler(state=get_info_about_order.person_number)
async def get_number(message: types.message, state: FSMContext):
    try:
        answer = message.contact.phone_number
        info_about_new_order[str(message.from_user.id)]['number'] = answer
    except AttributeError:
        answer = message.text
        info_about_new_order[str(message.from_user.id)]['number'] = answer
    await bot.send_message(chat_id=message.from_user.id, text='Введите адрес доставки:', reply_markup=main_btn)
    await get_info_about_order.person_adres.set()


@dp.message_handler(state=get_info_about_order.person_adres)
async def get_adres(message: types.Message, state: FSMContext):
    answer = message.text
    comment_butt = InlineKeyboardButton('Не указывать', callback_data='No_comment')
    comment_but = InlineKeyboardMarkup().add(comment_butt)
    info_about_new_order[str(message.from_user.id)]['adres'] = answer
    await bot.send_message(chat_id=message.from_user.id, text='Укажите комментарий к заказу:', reply_markup=comment_but)
    await get_info_about_order.order_comment.set()


@dp.message_handler(state=get_info_about_order.order_comment)
async def get_comment(message: types.Message, state: FSMContext):
    answer = message.text
    info_about_new_order[str(message.from_user.id)]['comment'] = answer
    await state.finish()
    await predcheck(info_about_new_order, message)


async def predcheck(info, message: types.Message):
    order_number = random.randint(100, 999)
    add_butt = InlineKeyboardButton('Подтвердить заказ', callback_data=f'accept_{order_number}_{message.from_user.id}')
    accept_but = InlineKeyboardMarkup().add(add_butt)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Номер вашего заказа {order_number}\n{about_order[str(message.from_user.id)]["info"]}\nАдрес доставки {info[str(message.from_user.id)]["adres"]}\nОплата наличными курьеру\nКомментарий к заказу: {info[str(message.from_user.id)]["comment"]}',
                           reply_markup=accept_but)
    about_order[str(message.from_user.id)]['order_number'] = order_number


async def send_order_to_restouran(contact, order, person_id):
    for id in admins_IDS:
        invite_butt = InlineKeyboardButton(f'Принять заказ {order[str(person_id)]["order_number"]}!',
                                           callback_data=f'invite_{order[str(person_id)]["order_number"]}_{person_id}')
        invite_but = InlineKeyboardMarkup().add(invite_butt)
        await bot.send_message(chat_id=id, text=f'Новый заказ #{order[str(person_id)]["order_number"]} !\n'
                                                f'{order[str(person_id)]["info"]}\n'
                                                f'Гость : {contact[str(person_id)]["name"]}\n'
                                                f'Адрес доставки : {contact[str(person_id)]["adres"]}\n'
                                                f'Номер телефона : {contact[str(person_id)]["number"]}\n'
                                                f'Комментарий к заказу: {contact[str(person_id)]["comment"]}\n'
                                                f'Username: {contact[str(person_id)]["who"]}',
                               reply_markup=invite_but)
        print(f'Пришёл заказ!')
    else:
        del about_order[str(person_id)]
        del info_about_new_order[str(person_id)]


async def send_messages_subscribes(list):
    count_sub = 0
    for id in await get_subscribes_id():
        await bot.send_photo(chat_id=id, photo=list[1], caption=list[0])
        count_sub += 1
    else:
        return count_sub
