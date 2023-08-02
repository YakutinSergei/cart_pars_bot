from datetime import datetime
import asyncpg

from environs import Env

env = Env()
env.read_env()


async def db_connect():
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.execute('''CREATE TABLE IF NOT EXISTS users(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                            username VARCHAR NOT NULL DEFAULT 'None',
                                                            connection_date TIMESTAMP DEFAULT 'now()',
                                                            tg_id BIGSERIAL,
                                                            admin BOOLEAN DEFAULT 'false',
                                                            premium BOOLEAN DEFAULT 'false',
                                                            premium_start_date TIMESTAMP,
                                                            premium_end_date TIMESTAMP);''')
        datetime.now()
        await conn.execute('''CREATE TABLE IF NOT EXISTS blockedUsers(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                               block_count INTEGER DEFAULT '0');''')

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')