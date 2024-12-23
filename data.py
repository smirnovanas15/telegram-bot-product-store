import sqlite3
import random

from buttons import create_buttons_types, create_buttons_dishes

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создание таблиц
cursor.execute('CREATE TABLE IF NOT EXISTS dishes_types(ID TEXT, name TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS dishes(ID TEXT, name TEXT,category TEXT,active TEXT, '
               'price TEXT, structure TEXT, weight TEXT, photo TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS work(min_cost TEXT,sale TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS subscribes(id TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS discount(activity TEXT, coast TEXT)')


async def add_dish_cat_to_base(title):
    cat_info = []
    category_id = random.randint(1, 999)
    cats = cursor.execute("SELECT ID FROM dishes_types")
    while category_id in cats:
        category_id = random.randint(1, 999)
    cat_info.insert(0, category_id)
    cat_info.insert(1, title)
    cursor.executemany(
        """INSERT INTO dishes_types(ID, name) VALUES (?, ?)""",
        (cat_info,))
    conn.commit()


async def get_all_categories(user_role):
    list_categories = []
    sql_select_query = """select * from dishes_types"""
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    try:
        for row in records:
            list_categories.append(row[1])
    except IndexError:
        pass
    finally:
        return await create_buttons_types(list_categories, user_role)


async def get_all_dishes():
    list_dishes = []
    sql_select_query = """select * from dishes"""
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    try:
        for row in records:
            list_dishes.append(row[1])
    except IndexError:
        pass
    finally:
        return await create_buttons_dishes(list_dishes)


async def add_dish_to_base(lst):
    dish_id = random.randint(1, 999)
    dishes = cursor.execute("SELECT ID FROM dishes")
    while dish_id in dishes:
        dish_id = random.randint(1, 999)
    lst.insert(0, dish_id)
    cursor.executemany("""INSERT INTO dishes(ID,name,category,active,price, structure, weight, photo) VALUES (
    ?,?,?,?,?,?,?,?)""", (lst,))
    conn.commit()


async def get_dish_with_type(category):
    dishes = {}
    request = """select * from dishes where category =?"""
    cursor.execute(request, (category,))
    records = cursor.fetchall()
    for dish in records:
        dishes[dish[1]] = {'Цена': round(float(dish[4]), 2),
                           'Состав': dish[5],
                           'Вес': dish[6],
                           'Фото': dish[7],
                           'id': dish[0]}
    else:
        return dishes


async def get_cat_list():
    list_categories = []
    sql_select_query = """select * from dishes_types"""
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    try:
        for row in records:
            list_categories.append(row[1])
    except IndexError:
        pass
    finally:
        return list_categories


async def get_dish_list():
    list_dishes = []
    sql_select_query = """select * from dishes"""
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    try:
        for row in records:
            list_dishes.append(row[1])
    except IndexError:
        pass
    finally:
        return list_dishes


async def remove_dish(title):
    request = """DELETE FROM dishes WHERE name = ?"""
    cursor.execute(request, (title,))
    conn.commit()


async def remove_cat(title):
    request = """DELETE FROM dishes_types WHERE name = ?"""
    cursor.execute(request, (title,))
    conn.commit()


async def search_dish(chat_id, id):
    from cart import add_dish_to_cart
    search = []
    request = """select * from dishes where id = ?"""
    cursor.execute(request, (id,))
    records = cursor.fetchall()
    for dish in records:
        search.append(dish[1])
        search.append(float(dish[4]))
    await add_dish_to_cart(chat_id, search)


async def set_deli_price(price):
    request = """select dil_price from work"""
    cursor.execute(request)
    records = cursor.fetchall()
    if len(records) > 0:
        sql = """Update work set dil_price = ?"""
        cursor.execute(sql, (price,))
        conn.commit()
    else:
        cursor.executemany(
            """INSERT INTO work (dil_price) VALUES (?)""",
            (price,))
        conn.commit()


async def get_deli_cost():
    cost = float
    request = """select dil_price from work"""
    cursor.execute(request)
    try:
        for i in cursor.fetchone():
            cost = i
            break
        return cost
    except TypeError:
        cost = 0
        return cost


async def set_min_order(price):
    request = """select min_cost from work"""
    cursor.execute(request)
    records = cursor.fetchall()
    if len(records) > 0:
        sql = """Update work set min_cost = ?"""
        cursor.execute(sql, (price,))
        conn.commit()
    else:
        cursor.executemany(
            """INSERT INTO work (min_cost) VALUES (?)""",
            (price,))
        conn.commit()


async def get_min_order():
    cost = float
    request = """select min_cost from work"""
    cursor.execute(request)
    try:
        for i in cursor.fetchone():
            cost = i
            break
        return cost
    except TypeError:
        cost = 0
        return cost


async def get_sale():
    request = """select sale from work"""
    cursor.execute(request)
    return cursor.fetchone()[0]

async def edit_sale(old,new):
    sql = """UPDATE work SET sale = ? WHERE sale = ?"""
    cursor.execute(sql,(new,old))
    conn.commit()



async def save_subscribe_id(id):
    request = """select * from subscribes"""
    cursor.execute(request)
    records = cursor.fetchall()
    if len(records) > 0:
        for ids in records:
            if id in ids:
                break
        else:
            cursor.execute(
                """INSERT INTO subscribes (id) VALUES (?)""",
                (id,))
            conn.commit()
    else:
        cursor.execute(
            """INSERT INTO subscribes (id) VALUES (?)""",
            (id,))
        conn.commit()


async def get_subscribes_id():
    list_subscribes = []
    request = """select * from subscribes"""
    cursor.execute(request)
    records = cursor.fetchall()
    for ids in records:
        list_subscribes.append(ids[0])
    else:
        return list_subscribes


async def set_discount(coast):
    request = """select * from discount"""
    cursor.execute(request)
    records = cursor.fetchall()
    if len(records) > 0:
        sql = """Update discount set activity = ?, coast = ?"""
        cursor.executemany(sql, (coast,))
        conn.commit()
    else:
        cursor.executemany(
            """INSERT INTO discount (activity,coast) VALUES (?,?)""",
            (coast,))
        conn.commit()


async def get_discount():
    cost = int
    request = """select coast from discount"""
    cursor.execute(request)
    try:
        for i in cursor.fetchone():
            cost = i
            break
        return int(cost)
    except TypeError:
        cost = 0
        return int(cost)


async def get_dish(dish):
    dish_dict = []
    request = """select * from dishes where name = ?"""
    cursor.execute(request, (dish,))
    records = cursor.fetchall()
    for dish_i in records:
        dish_dict.append(dish_i)
    else:
        return dish_dict
