import sqlite3
import aiosqlite
from contextlib import closing


class SqlLiteConnector:
    def __init__(self, connection):
        self.connection = connection
        print("Connected to SQLite Database...")

    # Connect class method to invoke on the bot instance
    # bot.connection = sqlite.SqlLiteConnector.connect('PATH')
    @classmethod
    def start_connection(cls, database_path):
        return cls(sqlite3.connect(database_path))

    def add_coins(self, user_id, coins):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute('UPDATE Users SET Coins=Coins + ? WHERE ID=?', (coins, str(user_id)))
            self.connection.commit()

    def remove_coins(self, user_id, coins):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute('UPDATE Users SET Coins=Coins - ? WHERE ID=?', (coins, str(user_id)))
            self.connection.commit()

    def remove_user_from_db(self, user_id):
        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.execute('DELETE FROM Users WHERE ID=?', (str(user_id),))
                self.connection.commit()
            except sqlite3.Error as e:
                print(e)

    def set_coins(self, user_id, coins):
        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.execute('UPDATE Users SET Coins=? WHERE ID=?', (coins, str(user_id)))
                self.connection.commit()
                return True
            except sqlite3.Error as e:
                print(e)

    def get_coins(self, user_id):
        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.execute('SELECT Coins FROM Users WHERE ID=?', (user_id,))
                row = cursor.fetchone()
                if row is None:
                    return 0
                else:
                    return row[0]
            except sqlite3.Error as e:
                print(e)
                return 0

    def get_all_users_coins(self):
        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.execute('SELECT Name, Coins FROM Users ORDER BY Coins DESC LIMIT 10')
                rows = cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                print(e)
                return 0

    def set_default_coins(self, user_id, name, coins=1000):
        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.execute('INSERT INTO Users (ID, Name, Coins) VALUES (?,?,?)', [str(user_id), name, coins])
                self.connection.commit()
                print(f"{name} has had their coins successfully added")
            # Don't need to print out the error for each member in the server.  This would become a huge
            # processing hog if the server ever became huge
            except sqlite3.Error:
                pass

