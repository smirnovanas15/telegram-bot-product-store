from data import search_dish, get_min_order, get_discount

total = {}
user_cart = {}

# Функция для генерации уникального идентификатора товара
async def create_id_dish(chat_id, dish):
    id = '' # Переменная для хранения идентификатора
    for i in dish: # Проходим по каждому символу в названии товара
        if i.isdigit(): # Если символ является цифрой
            id = id + i  # Добавляем эту цифру к идентификатору
    else:
        await search_dish(chat_id, id)  # Выполняем поиск блюда по его идентификатору

# Функция для добавления товара в корзину пользователя
async def add_dish_to_cart(chat_id, list): 
    discount = await get_discount() # Получаем текущую скидку
    global total
    if chat_id in user_cart:  # Если пользователь уже имеет корзину
        if list[0] in user_cart[chat_id]: # Если товар уже есть в корзине
            user_cart[chat_id][list[0]]['Кол-во'] += 1 # Увеличим количество этого блюда на 1
        else: # Если блюдо ещё не добавлено в корзину
            user_cart[chat_id][list[0]] ={ 
                'Цена': float(list[1]),
                'Кол-во': 1 }
    else: # Если у пользователя ещё нет корзины
        user_cart[chat_id] = {
            list[0]: {'Цена': round(list[1],2),
                                        'Кол-во': 1}
                                        }
    for k, v in user_cart[chat_id][list[0]].items():  # Проходим по элементам добавленного блюда
        if k == 'Цена':
            if chat_id in total: # Если общая сумма для этого пользователя уже существует
                total[chat_id] += float(v) # Добавляем цену блюда к общей сумме
            else:
                total[chat_id] = float(v) # Устанавливаем общую сумму равной цене первого блюда
    else: # После завершения цикла
        if discount <= 0: # Если скидка отсутствует
            user_cart[chat_id]['Итог'] = total[chat_id] # Итоговая сумма равна общей сумме без учёта скидки
        else:
            user_cart[chat_id]['Итог'] = total[chat_id]*(1 - discount / 100) # Применяем скидку к итоговой сумме

# Функция для формирования строки с содержимым корзины
async def cart_cr(user_id):
    reply = '' # Переменная для хранения сформированной строки
    discount = await get_discount() # Получаем текущую скидку
    global total
    from handlers import create_cart  # Импортируем функцию для создания корзины
    if str(user_id) not in user_cart: # Если у пользователя нет корзины
        return False
    for key, value in user_cart[str(user_id)].items(): # Проходим по всем товарам в корзине
        try:
            count = value['Кол-во'] # Получаем количество данного блюда
            if discount <= 0: # Если скидка отсутствует
                price = value['Цена'] # Цена блюда остаётся неизменной
            else: 
                price = value['Цена']*(1 - discount / 100) # Применяем скидку к цене товара
            coast = float(count * price) # Рассчитываем стоимость с учётом количества
            reply += f'{key} | {round(price,2)} RUB x {value["Кол-во"]} шт. | {round(coast,2)} RUB\n' # Формируем строку с информацией о блюде
        except TypeError:
            continue
    else:
        if discount <= 0:
            reply += f"Итог: {total[str(user_id)]} RUB"
            await create_cart(reply, user_id, total[str(user_id)])
        else:
            reply += f"Итог: {round(total[str(user_id)]*(1 - discount / 100),2)} RUB"
            await create_cart(reply, user_id, total[str(user_id)])
# Функция для очистки корзины пользователя
async def clear_cart(user_id):
    global total
    try:
        user_cart.pop(str(user_id))  # Удаляем корзину пользователя
        total[str(user_id)] = 0 # Обнуляем общую сумму для этого пользователя
    except KeyError: 
        pass
# Функция для сравнения общей суммы заказа с минимальной суммой заказа

async def compiration_prices(user_id):
    if float(await get_min_order()) <= total[str(user_id)]: # Если минимальная сумма меньше или равна общей сумме
        return True # Заказ может быть оформлен
    else:
        return False # Заказ не может быть оформлен



