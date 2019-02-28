import sqlite3
import asyncpg
import constants
from contextlib import closing


class DatabaseConnector:
    def __init__(self, db_string):
        self.db_string = db_string
        self.connection = None

    async def start_connection(self):
        self.connection = await asyncpg.connect(user="postgres", password=constants.password, database=self.db_string)
        print("Connected to PostGres Database...!")

    async def add_coins(self, user_id, coins):
        async with self.connection.transaction():
            await self.connection.execute('''UPDATE Users SET Coins=Coins + $1 WHERE ID=$2;''', coins, str(user_id))

    async def remove_coins(self, user_id, coins):
        async with self.connection.transaction():
            await self.connection.execute('''UPDATE Users SET Coins=Coins - $1 WHERE ID=$2;''', coins, str(user_id))

    async def remove_user_from_db(self, user_id):
        async with self.connection.transaction():
            try:
                await self.connection.execute('''DELETE FROM Users WHERE ID=$1;''', str(user_id))
            except asyncpg.DataError as e:
                print(e)
                return 0

    async def set_coins(self, user_id, coins):
        async with self.connection.transaction():
            try:
                cur = await self.connection.cursor('''UPDATE Users SET Coins=$1 WHERE ID=$2 RETURNING name, coins;''',
                                                   coins, str(user_id))
                row = await cur.fetchrow()
                return row
            except asyncpg.DataError as e:
                print(e)
                return 0

    async def get_coins(self, user_id: str):
        async with self.connection.transaction():
            try:
                cur = await self.connection.cursor('''SELECT Coins FROM Users WHERE ID=($1);''', str(user_id))
                row = await cur.fetchrow()
                if row is None:
                    return 0
                else:
                    return row[0]
            except asyncpg.DataError as e:
                print(e)
                return 0

    async def get_all_users_coins(self):
        async with self.connection.transaction():
            try:
                cur = await self.connection.cursor('''SELECT Name, Coins FROM Users ORDER BY Coins DESC''')
                rows = await cur.fetch(10)
                return rows
            except asyncpg.DataError as e:
                print(e)
                return 0

    async def set_default_coins(self, user_id, name, coins=1000):
        async with self.connection.transaction():
            await self.connection.execute('''
                INSERT INTO Users (id, name, coins) VALUES ($1, $2, $3);''', str(user_id), name, coins)
            print(f"{name} has had their coins successfully added")
