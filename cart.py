from data import search_dish, get_min_order, get_discount

total = {}
user_cart = {}


async def create_id_dish(chat_id, dish):
    id = ''
    for i in dish:
        if i.isdigit():
            id = id + i
    else:
        await search_dish(chat_id, id)


async def add_dish_to_cart(chat_id, list):
    discount = await get_discount()
    global total
    if chat_id in user_cart:
        if list[0] in user_cart[chat_id]:
            user_cart[chat_id][list[0]]['Кол-во'] += 1
        else:
            user_cart[chat_id][list[0]] = {
                'Цена': float(list[1]),
                'Кол-во': 1}
    else:
        user_cart[chat_id] = {list[0]: {'Цена': round(list[1],2),
                                        'Кол-во': 1}}
    for k, v in user_cart[chat_id][list[0]].items():
        if k == 'Цена':
            if chat_id in total:
                total[chat_id] += float(v)
            else:
                total[chat_id] = float(v)
    else:
        if discount <= 0:
            user_cart[chat_id]['Итог'] = total[chat_id]
        else:
            user_cart[chat_id]['Итог'] = total[chat_id]*(1 - discount / 100)


async def cart_cr(user_id):
    reply = ''
    discount = await get_discount()
    global total
    from handlers import create_cart
    if str(user_id) not in user_cart:
        return False
    for key, value in user_cart[str(user_id)].items():
        try:
            count = value['Кол-во']
            if discount <= 0:
                price = value['Цена']
            else:
                price = value['Цена']*(1 - discount / 100)
            coast = float(count * price)
            reply += f'{key} | {round(price,2)} RUB x {value["Кол-во"]} шт. | {round(coast,2)} RUB\n'
        except TypeError:
            continue
    else:
        if discount <= 0:
            reply += f"Итог: {total[str(user_id)]} RUB"
            await create_cart(reply, user_id, total[str(user_id)])
        else:
            reply += f"Итог: {round(total[str(user_id)]*(1 - discount / 100),2)} RUB"
            await create_cart(reply, user_id, total[str(user_id)])


async def clear_cart(user_id):
    global total
    try:
        user_cart.pop(str(user_id))
        total[str(user_id)] = 0
    except KeyError:
        pass


async def compiration_prices(user_id):
    if float(await get_min_order()) <= total[str(user_id)]:
        return True
    else:
        return False



