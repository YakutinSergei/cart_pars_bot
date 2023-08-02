import asyncpg

from environs import Env

env = Env()
env.read_env()


'''Добавление пользователей'''
async def add_user(tg_id, username):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))

        user = await conn.fetchrow(f"SELECT * FROM users WHERE tg_id={tg_id}")
        if not user:
            await conn.execute(f'''INSERT INTO users(tg_id, username) 
                              VALUES($1, $2)''',
                               tg_id, username)
            return 1
        else:
            return -1

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')


'''Получение списка админа'''
async def get_admin():
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))

        users_admin = await conn.fetch(f"SELECT * FROM users WHERE admin='True'")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return users_admin
            print('[INFO] PostgresSQL closed')


'''Поверка премиум статуса'''
async def check_premium(tg_id):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))

        user = await conn.fetchrow(f"SELECT * FROM users WHERE tg_id={tg_id}")

        if user['premium'] or user['admin']:
            return 1
        else:
            return -1


    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')