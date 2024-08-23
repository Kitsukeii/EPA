import os
import unittest
import sqlite3

class TestDbCreation(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_users.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()
        os.remove(self.db_path)
    
    def test_users_table_creation(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEST NOT NULL,
              password TEST NOT NULL
    )''')
        self.conn.commit()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table_exists = self.cursor.fetchone()
        self.assertIsNotNone(table_exists, "Users table exists")

        self.cursor.execute("PRAGMA table_info(users);")
        columns = [column[1] for column in self.cursor.fetchall()]
        self.assertIn('id', columns, "Table column exists")
        self.assertIn('username', columns, "Username column exists")
        self.assertIn('password', columns, "Passwords column exists")

if __name__ == '__main__':
    unittest.main()